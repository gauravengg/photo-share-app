from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import shutil
import os
from datetime import datetime
import uuid
from passlib.context import CryptContext
import json

from models import Person, Photo, ReferencePhoto, Event, get_db, init_db, photo_person
from face_recognition_service import FaceRecognitionService, validate_image
from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI(title="Smart Photo Share API")

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
face_service = FaceRecognitionService()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Directories
# Directories - use /tmp for Railway deployment
import os as os_module
UPLOAD_DIR = os_module.getenv("UPLOAD_DIR", "/tmp/uploads/originals")
FACES_DIR = os_module.getenv("FACES_DIR", "/tmp/uploads/faces")
THUMBNAIL_DIR = os_module.getenv("THUMBNAIL_DIR", "/tmp/uploads/thumbnails")

os_module.makedirs(UPLOAD_DIR, exist_ok=True)
os_module.makedirs(FACES_DIR, exist_ok=True)
os_module.makedirs(THUMBNAIL_DIR, exist_ok=True)
# Pydantic models for request/response
class UserRegister(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class PhotoResponse(BaseModel):
    id: int
    file_path: str
    thumbnail_path: Optional[str]
    uploaded_at: datetime
    people_count: int

class PersonResponse(BaseModel):
    id: int
    name: str
    email: str
    photo_count: int


# --- API Endpoints ---

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()
    print("✅ Server started successfully!")


@app.get("/")
async def root():
    return {"message": "Smart Photo Share API", "status": "running"}


# --- User Management ---

@app.post("/api/register")
async def register_user(user: UserRegister, db: Session = Depends(get_db)):
    """Register a new user"""
    # Check if user exists
    existing_user = db.query(Person).filter(Person.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    hashed_password = pwd_context.hash(user.password)
    new_person = Person(
        name=user.name,
        email=user.email,
        password_hash=hashed_password
    )
    
    db.add(new_person)
    db.commit()
    db.refresh(new_person)
    
    return {"message": "User registered successfully", "user_id": new_person.id}


@app.post("/api/login")
async def login_user(user: UserLogin, db: Session = Depends(get_db)):
    """Login user"""
    person = db.query(Person).filter(Person.email == user.email).first()
    
    if not person or not pwd_context.verify(user.password, person.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return {
        "message": "Login successful",
        "user_id": person.id,
        "name": person.name,
        "has_face_data": person.face_embeddings is not None
    }


# --- Face Enrollment ---

@app.post("/api/enroll-face/{user_id}")
async def enroll_face(
    user_id: int,
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    """
    Enroll user's face by uploading 3-5 reference photos
    """
    person = db.query(Person).filter(Person.id == user_id).first()
    if not person:
        raise HTTPException(status_code=404, detail="User not found")
    
    if len(files) < 3:
        raise HTTPException(status_code=400, detail="Please upload at least 3 photos")
    
    enrolled_count = 0
    
    for file in files:
        # Save file
        file_ext = os.path.splitext(file.filename)[1]
        unique_filename = f"{user_id}_{uuid.uuid4()}{file_ext}"
        file_path = os.path.join(FACES_DIR, unique_filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Detect face and extract encoding
        face_encodings, face_locations = face_service.detect_faces(file_path)
        
        if not face_encodings:
            os.remove(file_path)  # Remove file if no face detected
            continue
        
        # Take the first (and hopefully only) face
        encoding = face_encodings[0]
        
        # Save reference photo record
        ref_photo = ReferencePhoto(
            person_id=user_id,
            file_path=file_path
        )
        db.add(ref_photo)
        
        # Add encoding to person
        person.add_face_embedding(encoding)
        enrolled_count += 1
    
    if enrolled_count == 0:
        raise HTTPException(status_code=400, detail="No faces detected in uploaded photos")
    
    db.commit()
    
    return {
        "message": f"Successfully enrolled {enrolled_count} face samples",
        "enrolled_count": enrolled_count
    }


# --- Photo Upload and Processing ---

@app.post("/api/upload-photos")
async def upload_photos(
    files: List[UploadFile] = File(...),
    uploaded_by: int = Form(...),
    event_name: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """
    Upload multiple photos for processing
    """
    uploader = db.query(Person).filter(Person.id == uploaded_by).first()
    if not uploader:
        raise HTTPException(status_code=404, detail="User not found")
    
    uploaded_photos = []
    
    for file in files:
        if not validate_image(file.filename):
            continue
        
        # Save original photo
        file_ext = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Create thumbnail
        thumbnail_path = os.path.join(THUMBNAIL_DIR, f"thumb_{unique_filename}")
        face_service.create_thumbnail(file_path, thumbnail_path)
        
        # Create photo record
        photo = Photo(
            file_path=file_path,
            thumbnail_path=thumbnail_path,
            uploaded_by=uploaded_by,
            event_name=event_name,
            processed=0  # Mark as pending
        )
        
        db.add(photo)
        db.commit()
        db.refresh(photo)
        
        uploaded_photos.append(photo.id)
    
    return {
        "message": f"Uploaded {len(uploaded_photos)} photos",
        "photo_ids": uploaded_photos
    }


@app.post("/api/process-photos")
async def process_photos(db: Session = Depends(get_db)):
    """
    Process all pending photos: detect faces and match with enrolled people
    """
    # Get all people with face encodings
    people = db.query(Person).filter(Person.face_embeddings.isnot(None)).all()
    
    people_encodings = {}
    for person in people:
        encodings = person.get_face_embeddings()
        if encodings:
            # Convert back to numpy arrays
            import numpy as np
            people_encodings[person.id] = [np.array(enc) for enc in encodings]
    
    # Get pending photos
    pending_photos = db.query(Photo).filter(Photo.processed == 0).all()
    
    processed_count = 0
    
    for photo in pending_photos:
        try:
            # Process photo
            result = face_service.process_photo(photo.file_path, people_encodings)
            
            # Link photo to identified people
            for identified in result['identified_people']:
                person_id = identified['person_id']
                confidence = identified['confidence']
                
                # Add relationship
                person = db.query(Person).filter(Person.id == person_id).first()
                if person and person not in photo.people:
                    photo.people.append(person)
                    
                    # Store confidence in association table
                    db.execute(
                        photo_person.update().where(
                            (photo_person.c.photo_id == photo.id) &
                            (photo_person.c.person_id == person_id)
                        ).values(confidence=confidence)
                    )
            
            photo.processed = 1
            processed_count += 1
            
        except Exception as e:
            print(f"Error processing photo {photo.id}: {e}")
            photo.processed = -1  # Mark as failed
    
    db.commit()
    
    return {
        "message": f"Processed {processed_count} photos",
        "processed_count": processed_count
    }


# --- Photo Retrieval ---

@app.get("/api/my-photos/{user_id}")
async def get_my_photos(user_id: int, db: Session = Depends(get_db)):
    """Get all photos where this user appears"""
    person = db.query(Person).filter(Person.id == user_id).first()
    if not person:
        raise HTTPException(status_code=404, detail="User not found")
    
    photos = person.photos
    
    return {
        "total_photos": len(photos),
        "photos": [
            {
                "id": photo.id,
                "thumbnail_path": photo.thumbnail_path,
                "uploaded_at": photo.uploaded_at.isoformat(),
                "event_name": photo.event_name
            }
            for photo in photos
        ]
    }


@app.get("/api/photo/{photo_id}")
async def get_photo(photo_id: int, db: Session = Depends(get_db)):
    """Get full resolution photo"""
    photo = db.query(Photo).filter(Photo.id == photo_id).first()
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    
    return FileResponse(photo.file_path)


@app.get("/api/thumbnail/{photo_id}")
async def get_thumbnail(photo_id: int, db: Session = Depends(get_db)):
    """Get photo thumbnail"""
    photo = db.query(Photo).filter(Photo.id == photo_id).first()
    if not photo or not photo.thumbnail_path:
        raise HTTPException(status_code=404, detail="Thumbnail not found")
    
    return FileResponse(photo.thumbnail_path)


# --- Statistics ---

@app.get("/api/stats")
async def get_stats(db: Session = Depends(get_db)):
    """Get system statistics"""
    total_users = db.query(Person).count()
    total_photos = db.query(Photo).count()
    processed_photos = db.query(Photo).filter(Photo.processed == 1).count()
    pending_photos = db.query(Photo).filter(Photo.processed == 0).count()
    
    return {
        "total_users": total_users,
        "total_photos": total_photos,
        "processed_photos": processed_photos,
        "pending_photos": pending_photos
    }

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
