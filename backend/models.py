from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Table, LargeBinary, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
import json

Base = declarative_base()

# Association table for many-to-many relationship between photos and people
photo_person = Table('photo_person', Base.metadata,
    Column('photo_id', Integer, ForeignKey('photos.id')),
    Column('person_id', Integer, ForeignKey('people.id')),
    Column('confidence', Float, default=0.0)  # Match confidence score
)

class Person(Base):
    __tablename__ = 'people'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Store multiple face embeddings as JSON (for different angles/lighting)
    face_embeddings = Column(String, nullable=True)  # JSON array of embeddings
    
    # Relationships
    photos = relationship('Photo', secondary=photo_person, back_populates='people')
    reference_photos = relationship('ReferencePhoto', back_populates='person')
    
    def add_face_embedding(self, embedding):
        """Add a new face embedding for this person"""
        embeddings = self.get_face_embeddings()
        embeddings.append(embedding.tolist())
        self.face_embeddings = json.dumps(embeddings)
    
    def get_face_embeddings(self):
        """Get all face embeddings for this person"""
        if not self.face_embeddings:
            return []
        return json.loads(self.face_embeddings)


class ReferencePhoto(Base):
    """Reference photos uploaded during enrollment"""
    __tablename__ = 'reference_photos'
    
    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey('people.id'))
    file_path = Column(String(500), nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    
    person = relationship('Person', back_populates='reference_photos')


class Photo(Base):
    __tablename__ = 'photos'
    
    id = Column(Integer, primary_key=True)
    file_path = Column(String(500), nullable=False)
    thumbnail_path = Column(String(500))
    uploaded_by = Column(Integer, ForeignKey('people.id'))
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    processed = Column(Integer, default=0)  # 0=pending, 1=processed, -1=failed
    event_name = Column(String(200))  # Optional: group photos by event
    
    # Relationships
    people = relationship('Person', secondary=photo_person, back_populates='photos')
    uploader = relationship('Person', foreign_keys=[uploaded_by])


class Event(Base):
    """Optional: Group photos into events"""
    __tablename__ = 'events'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    description = Column(String(500))
    date = Column(DateTime)
    created_by = Column(Integer, ForeignKey('people.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    share_code = Column(String(50), unique=True)  # For easy sharing


# Database setup
DATABASE_URL = "sqlite:///./photo_share.db"  # Using SQLite for easy setup, can switch to PostgreSQL later

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")

def get_db():
    """Dependency for FastAPI routes"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
