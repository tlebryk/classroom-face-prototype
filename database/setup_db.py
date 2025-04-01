#!/usr/bin/env python3

import json
import os
import sqlite3
import shutil
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def setup_database(db_path, students_json, images_dir=None, images_output_dir=None):
    try:
        with open(students_json, 'r') as f:
            students = json.load(f)
        logger.info(f"Loaded information for {len(students)} students")
    except (json.JSONDecodeError, FileNotFoundError) as e:
        logger.error(f"Failed to load students.json: {e}")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            studentId TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            photoReference TEXT
        )
    """)
    
    inserted_count = 0
    for student in students:
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO students (studentId, name, email, photoReference)
                VALUES (?, ?, ?, ?)
            """, (
                student["studentId"],
                student["name"],
                student["email"],
                student["photoReference"]
            ))
            inserted_count += 1
        except sqlite3.Error as e:
            logger.error(f"Error inserting student {student.get('studentId')}: {e}")
    
    conn.commit()
    logger.info(f"Inserted or updated {inserted_count} student records")
    
    if images_dir and images_output_dir:
        if not os.path.exists(images_output_dir):
            os.makedirs(images_output_dir)
            
        copied_count = 0
        for student in students:
            photo_ref = student.get("photoReference")
            if not photo_ref:
                continue
                
            found_file = None
            for ext in ["", ".jpg", ".jpeg", ".png"]:
                src_path = os.path.join(images_dir, photo_ref + ext)
                if os.path.exists(src_path):
                    found_file = src_path
                    break
            
            if found_file:
                dst_path = os.path.join(images_output_dir, os.path.basename(found_file))
                try:
                    shutil.copy2(found_file, dst_path)
                    copied_count += 1
                except (shutil.Error, IOError) as e:
                    logger.error(f"Error copying image {photo_ref}: {e}")
            else:
                logger.warning(f"Could not find image for {student.get('studentId')} ({photo_ref})")
        
        logger.info(f"Copied {copied_count} images to {images_output_dir}")
    
    conn.close()
    logger.info("Database setup complete")

if __name__ == "__main__":
    db_path = os.environ.get("DATABASE_PATH", "students.db")
    students_json = os.environ.get("STUDENTS_JSON", "students.json")
    images_dir = os.environ.get("IMAGES_DIR", "/data/images")
    images_output_dir = os.environ.get("IMAGES_OUTPUT_DIR")
    
    setup_database(db_path, students_json, images_dir, images_output_dir)