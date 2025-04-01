import os
import numpy as np
import cv2
from deepface import DeepFace
from sklearn.metrics.pairwise import cosine_similarity
import logging
import requests
from typing import Dict, Any, Optional

class FaceRecognizer:
    
    def __init__(self, reference_dir="reference_faces", similarity_threshold=0.4, 
                 database_url="http://localhost:5002"):
        self.reference_dir = reference_dir
        self.similarity_threshold = similarity_threshold
        self.database_url = database_url
        self.db_embeddings = []
        self.db_student_ids = []
        self.build_reference_database()
        
    def build_reference_database(self) -> None:
        logging.info(f"Building face database from: {self.reference_dir}")
        
        if not os.path.exists(self.reference_dir):
            os.makedirs(self.reference_dir)
            logging.warning(f"Created empty reference directory: {self.reference_dir}")
            return
            
        for filename in os.listdir(self.reference_dir):
            if filename.lower().endswith((".jpg", ".jpeg", ".png")):
                student_id = os.path.splitext(filename)[0]
                img_path = os.path.join(self.reference_dir, filename)
                
                try:
                    img = cv2.imread(img_path)
                    if img is None:
                        logging.error(f"Failed to load image: {img_path}")
                        continue
            
                    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    embedding = self.extract_embedding(img_rgb)
                    self.db_embeddings.append(embedding)
                    self.db_student_ids.append(student_id)
                    logging.info(f"Added {student_id} to face database")
                    
                except Exception as e:
                    logging.error(f"Error processing {img_path}: {str(e)}")
        
        if self.db_embeddings:
            self.db_embeddings = np.array(self.db_embeddings)
            logging.info(f"Face database built with {len(self.db_student_ids)} people")
        else:
            logging.warning("No valid reference faces found in directory")
    
    def extract_embedding(self, img_rgb: np.ndarray) -> np.ndarray:
        if img_rgb.dtype != np.uint8:
            img_rgb = (img_rgb * 255).astype(np.uint8)
            
        result = DeepFace.represent(
            img_path=img_rgb,
            model_name="ArcFace",
            detector_backend="opencv",
            enforce_detection=False,
            align=True
        )
        
        return np.array(result[0]["embedding"])
    
    def get_student_info(self, student_id: str) -> Optional[Dict[str, Any]]:
        try:
            response = requests.get(f"{self.database_url}/api/student?studentId={student_id}")
            if response.status_code == 200:
                return response.json()
            else:
                logging.error(f"Failed to fetch student {student_id}: {response.text}")
                return None
        except requests.RequestException as e:
            logging.error(f"Error connecting to database service: {e}")
            return None
    
    def recognize_face(self, img_rgb: np.ndarray) -> Dict[str, Any]:
        if len(self.db_embeddings) == 0 or not self.db_student_ids:
            return {
                "match": False,
                "error": "No reference faces available in database"
            }
        
        try:
            query_embedding = self.extract_embedding(img_rgb)
            
            similarities = cosine_similarity([query_embedding], self.db_embeddings)[0]
            
            best_match_idx = np.argmax(similarities)
            best_match_score = similarities[best_match_idx]
            
            all_scores = {student_id: float(score) for student_id, score 
                         in zip(self.db_student_ids, similarities)}
            
            if best_match_score >= self.similarity_threshold:
                student_id = self.db_student_ids[best_match_idx]
                
                student_info = self.get_student_info(student_id)
                
                return {
                    "match": True,
                    "similarity": float(best_match_score * 100),
                    "studentId": student_id,
                    "studentInfo": student_info,
                    "allScores": all_scores
                }
            else:
                return {
                    "match": False,
                    "similarity": float(best_match_score * 100),
                    "message": "No face matched above the similarity threshold",
                    "allScores": all_scores
                }
                
        except Exception as e:
            logging.error(f"Error in face recognition: {str(e)}")
            return {
                "match": False,
                "error": str(e)
            }
