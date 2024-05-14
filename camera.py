import cv2
import face_recognition
import time
import tkinter as tk
from tkinter import messagebox
import pyautogui
import vlc

def show_alert():
    root = tk.Tk() 
    root.attributes("-topmost", True)  # Ensure the alert window is on top
    root.withdraw()  # Hide the tkinter window
    tk.messagebox.showwarning("Face Not Detected ", "Face not detected for more than 5 seconds!")
    root.destroy()  # Destroy the tkinter window after showing the alert

    # Freeze the screen
    pyautogui.press('space')

def draw_landmarks(frame, landmarks):
    for landmark_type in landmarks:
        for point in landmarks[landmark_type]:
            cv2.circle(frame, point, 2, (0, 0, 255), -1)

def init():
    cap = cv2.VideoCapture(0)

    duration_gone = 0  # Timer to track how long the face is not detected
    alert_displayed = False  # Flag to track if alert message is displayed
    gone_time = -1

    while True:
        start_time = time.time()  # Start time of the loop iteration

        # Capture frame-by-frame
        ret, frame = cap.read()

        rgb_frame = frame[:, :, ::-1]
        # Find all the faces in the current frame of video
        face_locations = face_recognition.face_locations(rgb_frame)
        face_landmarks = face_recognition.face_landmarks(rgb_frame)

        if face_locations or alert_displayed:
            # Reset the timer if face is detected
            duration_gone = 0
            gone_time = -1
            alert_displayed = False

            for landmarks in face_landmarks:
                draw_landmarks(frame, landmarks)
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

        # Calculate the time taken for the loop iteration
        iteration_time = time.time() - start_time

        # Introduce a delay to control frame rate
        if iteration_time < 0.04:  # Adjust the value as needed for desired frame rate
            time.sleep(0.04 - iteration_time)

    cap.release()
    player.release()
    cv2.destroyAllWindows()

init()
