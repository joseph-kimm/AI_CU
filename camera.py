import cv2
import face_recognition
import time
import tkinter as tk
from tkinter import messagebox

def show_alert():
    root = tk.Tk()
    root.attributes("-topmost", True)  # Ensure the alert window is on top
    root.withdraw()  # Hide the tkinter window
    tk.messagebox.showwarning("Face Not Detected", "Face not detected for more than 5 seconds!")
    root.destroy()  # Destroy the tkinter window after showing the alert

def init():
    cap = cv2.VideoCapture(0)

    duration_gone = 0 # Timer to track how long the face is not detected
    alert_displayed = False  # Flag to track if alert message is displayed
    gone_time = -1

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        rgb_frame = frame[:, :, ::-1]
        # Find all the faces in the current frame of video
        face_locations = face_recognition.face_locations(rgb_frame)

        if face_locations:
            # Reset the timer if face is detected
            duration_gone = 0
            gone_time = -1
            alert_displayed = False
            for top, right, bottom, left in face_locations:
                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        else:
            # Increment the timer if face is not detected
            if duration_gone == 0:
                gone_time = time.time()
            duration_gone += 1

        # Display the resulting image
        cv2.imshow('Video', frame)

        elapsed_time = 0
        if gone_time >= 0:
            elapsed_time = time.time() - gone_time

        # Display alert message if face is not detected for more than 5 seconds
        if elapsed_time >= 5 and not alert_displayed:
            show_alert()
            alert_displayed = True

        # press Enter to exit
        if cv2.waitKey(25) == 13:
            break

    cap.release()
    cv2.destroyAllWindows()

init()
