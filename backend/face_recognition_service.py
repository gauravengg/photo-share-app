import face_recognition
import numpy as np
from PIL import Image
import os
from typing import List, Tuple, Dict
import cv2

class FaceRecognitionService:
    """Service for face detection and recognition"""
    
    def __init__(self, tolerance=0.6):
        """
        Initialize face recognition service
        
        Args:
            tolerance: Lower is more strict. 0.6 is good default.
        """
        self.tolerance = tolerance
    
    def detect_faces(self, image_path: str) -> List[np.ndarray]:
        """
        Detect all faces in an image and return their encodings
        
        Args:
            image_path: Path to the image file
            
        Returns:
            List of face encodings (128-dimensional vectors)
        """
        try:
            # Load image
            image = face_recognition.load_image_file(image_path)
            
            # Find all face locations and encodings
            face_locations = face_recognition.face_locations(image)
            face_encodings = face_recognition.face_encodings(image, face_locations)
            
            return face_encodings, face_locations
        except Exception as e:
            print(f"Error detecting faces in {image_path}: {e}")
            return [], []
    
    def extract_face_crop(self, image_path: str, face_location: Tuple[int, int, int, int], 
                          output_path: str) -> bool:
        """
        Crop and save a face from an image
        
        Args:
            image_path: Path to source image
            face_location: (top, right, bottom, left) coordinates
            output_path: Where to save the cropped face
            
        Returns:
            True if successful
        """
        try:
            image = Image.open(image_path)
            top, right, bottom, left = face_location
            
            # Add some padding
            padding = 20
            left = max(0, left - padding)
            top = max(0, top - padding)
            right = min(image.width, right + padding)
            bottom = min(image.height, bottom + padding)
            
            face_image = image.crop((left, top, right, bottom))
            face_image.save(output_path)
            return True
        except Exception as e:
            print(f"Error cropping face: {e}")
            return False
    
    def match_face(self, unknown_encoding: np.ndarray, 
                   known_encodings: List[np.ndarray]) -> Tuple[bool, float]:
        """
        Match a face encoding against known encodings
        
        Args:
            unknown_encoding: Face encoding to identify
            known_encodings: List of known face encodings to compare against
            
        Returns:
            (is_match, confidence_score)
        """
        if not known_encodings:
            return False, 0.0
        
        # Calculate face distances
        face_distances = face_recognition.face_distance(known_encodings, unknown_encoding)
        
        # Get the best match
        best_match_index = np.argmin(face_distances)
        best_distance = face_distances[best_match_index]
        
        # Convert distance to confidence (inverse relationship)
        confidence = 1 - best_distance
        
        # Check if match is good enough
        is_match = best_distance <= self.tolerance
        
        return is_match, confidence
    
    def identify_person(self, unknown_encoding: np.ndarray, 
                       people_encodings: Dict[int, List[np.ndarray]]) -> Tuple[int, float]:
        """
        Identify which person an unknown face belongs to
        
        Args:
            unknown_encoding: Face encoding to identify
            people_encodings: Dict mapping person_id to list of their face encodings
            
        Returns:
            (person_id, confidence) or (None, 0.0) if no match
        """
        best_person_id = None
        best_confidence = 0.0
        
        for person_id, encodings in people_encodings.items():
            is_match, confidence = self.match_face(unknown_encoding, encodings)
            
            if is_match and confidence > best_confidence:
                best_confidence = confidence
                best_person_id = person_id
        
        return best_person_id, best_confidence
    
    def create_thumbnail(self, image_path: str, output_path: str, size=(400, 400)):
        """Create a thumbnail of an image"""
        try:
            image = Image.open(image_path)
            image.thumbnail(size, Image.Resampling.LANCZOS)
            image.save(output_path)
            return True
        except Exception as e:
            print(f"Error creating thumbnail: {e}")
            return False
    
    def process_photo(self, image_path: str, people_encodings: Dict[int, List[np.ndarray]]) -> Dict:
        """
        Process a photo: detect faces and identify people
        
        Args:
            image_path: Path to the photo
            people_encodings: Dict mapping person_id to their face encodings
            
        Returns:
            Dict with detected people and their confidence scores
        """
        face_encodings, face_locations = self.detect_faces(image_path)
        
        results = {
            'total_faces': len(face_encodings),
            'identified_people': [],
            'unidentified_faces': 0
        }
        
        for encoding in face_encodings:
            person_id, confidence = self.identify_person(encoding, people_encodings)
            
            if person_id:
                results['identified_people'].append({
                    'person_id': person_id,
                    'confidence': float(confidence)
                })
            else:
                results['unidentified_faces'] += 1
        
        return results


# Utility functions
def validate_image(file_path: str) -> bool:
    """Check if file is a valid image"""
    valid_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}
    ext = os.path.splitext(file_path)[1].lower()
    return ext in valid_extensions


def get_file_hash(file_path: str) -> str:
    """Generate a hash for a file (to detect duplicates)"""
    import hashlib
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()
