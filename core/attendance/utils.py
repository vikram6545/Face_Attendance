import face_recognition
import cv2
import numpy as np
import os

def verify_face(known_image_path, captured_image_path):
    """
    Dlib/Face_Recognition use karke do photos ko 128-point encoding se match karta hai.
    """
    try:
        # 1. Check karo ki dono files exist karti hain
        if not os.path.exists(known_image_path) or not os.path.exists(captured_image_path):
            print(f"DEBUG Error: File nahi mili - {known_image_path} ya {captured_image_path}")
            return False

        # 2. Images load karo (Face recognition RGB format use karta hai)
        img_known = face_recognition.load_image_file(known_image_path)
        img_captured = face_recognition.load_image_file(captured_image_path)

        # 3. Face Encodings nikaalo (Yeh chehre ka digital signature hai)
        known_encodings = face_recognition.face_encodings(img_known)
        captured_encodings = face_recognition.face_encodings(img_captured)

        # 4. Check karo ki dono photos mein chehra mila bhi ya nahi
        if len(known_encodings) == 0:
            print("DEBUG: Database wali photo mein chehra nahi mila!")
            return False
        if len(captured_encodings) == 0:
            print("DEBUG: Camera wali photo mein chehra nahi mila!")
            return False

        # 5. Dono chehron ko compare karo
        # tolerance=0.5 (jitna kam, utni sakht matching)
        match = face_recognition.compare_faces([known_encodings[0]], captured_encodings[0], tolerance=0.5)
        
        # Distance check (Accuracy dekhne ke liye)
        face_distance = face_recognition.face_distance([known_encodings[0]], captured_encodings[0])
        
        print(f"---------- DEBUG INFO ----------")
        print(f"FACE DISTANCE: {face_distance[0]:.4f}")
        print(f"MATCH STATUS: {match[0]}")
        print(f"--------------------------------")

        if match[0]:
            print("---------- SUCCESS: IDENTITY MATCHED ----------")
            return True
        else:
            print("---------- FAIL: FACE MISMATCH ----------")
            return False

    except Exception as e:
        print(f"DEBUG Error: {str(e)}")
        return False