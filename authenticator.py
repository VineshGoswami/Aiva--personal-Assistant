import os
import cv2
import mediapipe as mp
import numpy as np
import pymongo
import pickle
import bcrypt
from PIL import Image

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["AivaDB"]
users_collection = db["users"]

mp_face_mesh = mp.solutions.face_mesh


def facelandmarks(image_array):
    with mp_face_mesh.FaceMesh(static_image_mode=True, refine_landmarks=True) as face_mesh:
        results = face_mesh.process(image_array)
        if not results.multi_face_landmarks:
            return None
        face_landmarks = results.multi_face_landmarks[0]
        return np.array([[lm.x, lm.y, lm.z] for lm in face_landmarks.landmark]).flatten()


def facelandmarksimg(image_path):
    image_path = image_path.strip().strip('"')
    if not os.path.exists(image_path):
        return None
    try:
        img = Image.open(image_path).convert('RGB')
        img_array = np.array(img)
        return facelandmarks(img_array)
    except:
        return None


def captureface():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return None

    frame = None
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        cv2.imshow("Face Capture - Press SPACE to capture", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == 32:
            break
        elif key == 27:
            cap.release()
            cv2.destroyAllWindows()
            return None

    cap.release()
    cv2.destroyAllWindows()

    if frame is None:
        return None

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return facelandmarks(frame_rgb)


def register(username, password, img_path=None, security_question=None, security_answer=None):
    if users_collection.find_one({"username": username}):
        return "Username already exists. Choose another."

    hashed_pwd = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    face_data = None
    if img_path:
        face_data = facelandmarksimg(img_path)
        if face_data is None or face_data.size == 0:
            return "No face detected. Try another image."

    hashed_answer = bcrypt.hashpw(security_answer.encode(), bcrypt.gensalt()).decode() if security_answer else None

    users_collection.insert_one({
        "username": username,
        "password": hashed_pwd,
        "face_encoding": pickle.dumps(face_data) if face_data is not None else None,
        "security_question": security_question,
        "security_answer": hashed_answer
    })

    print("Signup successful! You must log in again to continue.")

    while True:
        print("Login Options:")
        print("1. Login with Face")
        print("2. Login with Password")

        choice = input("Choose an option (1/2): ").strip()

        if choice == "1":
            login_message = login(username, use_face=True)
        elif choice == "2":
            password_attempt = input("Enter your password: ")
            login_message = login(username, password_attempt)
        else:
            print("Invalid choice. Try again.")
            continue

        print(login_message)

        if "Login successful" in login_message:
            print("\nStarting AIVA...")
            return login_message
        else:
            print("Authentication failed. Try again.")


def faceverify(stored_data):
    stored_data = pickle.loads(stored_data)
    live_data = captureface()
    if live_data is None:
        return False
    distance = np.linalg.norm(stored_data - live_data)
    return distance < 0.6


def get_security_question(username):
    user_data = users_collection.find_one({"username": username})
    if user_data and "security_question" in user_data:
        return user_data["security_question"]
    return None


def verify_security_answer(username, answer):
    user_data = users_collection.find_one({"username": username})
    if user_data and "security_answer" in user_data:
        return bcrypt.checkpw(answer.encode(), user_data["security_answer"].encode())
    return False


def login(username, password=None, use_face=False, image_path=None):
    user_data = users_collection.find_one({"username": username})
    if not user_data:
        return "User not found."

    if use_face:
        if user_data["face_encoding"] is None:
            return "Face authentication not set up. Use password login."

        if image_path:
            face_data = facelandmarksimg(image_path)
        else:
            face_data = captureface()

        if face_data is None:
            return "Failed to capture face. Try again."

        stored_face_data = pickle.loads(user_data["face_encoding"])
        distance = np.linalg.norm(stored_face_data - face_data)

        if distance < 0.6:
            return f"Login successful. Welcome, {username}!"
        else:
            print("Face authentication failed. Answer security question.")
            security_question = get_security_question(username)
            if security_question:
                print(f"Security Question: {security_question}")
                answer = input("Enter your answer: ").strip()
                if verify_security_answer(username, answer):
                    return f"Login successful via security question. Welcome, {username}!"
                else:
                    return "Incorrect security answer."
            return "Face authentication failed."

    else:
        stored_password = user_data["password"]
        if isinstance(stored_password, str):
            stored_password = stored_password.encode()

        try:
            if bcrypt.checkpw(password.encode(), stored_password):
                return f"Login successful. Welcome, {username}!"
            else:
                return "Incorrect password."
        except ValueError:
            print("Error: Password hash is corrupted. Resetting password is required.")
            return "Stored password is invalid. Please reset your password."
