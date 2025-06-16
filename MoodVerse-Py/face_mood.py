import cv2
import numpy as np
from deepface import DeepFace
import threading
import time
import requests

face_cascade = cv2.CascadeClassifier("D:/MoodVerse-Py/haarcascade_frontalface_default.xml")


cap = cv2.VideoCapture(0)

current_mood = ""
mood_detected = False
analyzing = False
frame_lock = threading.Lock()

api_url = "http://localhost:5000/mood-update"

def analyze_mood(face_roi):
    global current_mood, mood_detected, analyzing
    analyzing = True
    try:
        result = DeepFace.analyze(face_roi, actions=['emotion'], enforce_detection=False)
        dominant_emotion = result[0]['dominant_emotion']
        current_mood = dominant_emotion
        send_mood_to_api(dominant_emotion)
        mood_detected = True
        print(f"Mood detected: {dominant_emotion}")
    except Exception as e:
        print(f"Error analyzing mood: {e}")
    finally:
        analyzing = False

def send_mood_to_api(mood):
    try:
        response = requests.post(api_url, json={"mood": mood})
        if response.status_code == 200:
            print(f"Successfully sent mood: {mood}")
        else:
            print(f"Failed to send mood: {response.status_code}")
    except Exception as e:
        print(f"Error sending mood: {e}")

def detect_faces(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return face_cascade.detectMultiScale(gray, 1.3, 5)

def draw_feedback(frame, faces):
    global current_mood

    mood_colors = {
        "happy": (0, 255, 0),
        "sad": (255, 0, 0),
        "angry": (0, 0, 255),
        "fear": (255, 165, 0),
        "surprise": (255, 255, 0),
        "neutral": (200, 200, 200)
    }

    feedback_text = "Detecting mood..." if not mood_detected else f"Mood: {current_mood.upper()}"
    text_color = mood_colors.get(current_mood, (255, 255, 255))

    for (x, y, w, h) in faces:
        box_color = text_color
        cv2.rectangle(frame, (x, y), (x + w, y + h), box_color, 2)


    cv2.putText(frame, feedback_text, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.0, text_color, 2)
    return frame

def process_frame():
    global analyzing

    ret, frame = cap.read()
    if not ret:
        return

    faces = detect_faces(frame)

    if not mood_detected and not analyzing and len(faces) > 0:
        x, y, w, h = faces[0]
        face_roi = frame[y:y+h, x:x+w]
        threading.Thread(target=analyze_mood, args=(face_roi,)).start()

    with frame_lock:
        frame = draw_feedback(frame, faces)
        cv2.imshow("MoodVerse Scanner", frame)

def main():
    print("Launching MoodVerse Scanner...")
    
    print("Please wait for 3 seconds...")
    time.sleep(5)  # Wait for 5 seconds
    
    print("Starting mood scanning...")
    while True:
        process_frame()

        if mood_detected:
            time.sleep(3)
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
    print("MoodVerse Scanner closed.")