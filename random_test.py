import cv2
import face_recognition
import time
import tkinter as tk
from tkinter import messagebox

def multiVideo():

    # Define the video file path
    video_path = 'nba.mp4'

    # Create multiple VideoCapture instances
    cap1 = cv2.VideoCapture(video_path)

    # Check if the video capture objects were successfully opened
    if not cap1.isOpened():
        print("Error: Could not open video.")
        exit()

    # Create separate windows for displaying frames
    cv2.namedWindow('Video 1')
    cv2.namedWindow('Video 2')

    while True:
        # Read frames from each VideoCapture instance
        ret1, frame1 = cap1.read()
        #ret2, frame2 = cap2.read()

        # Check if frames were successfully read
        if not ret1:
            break

        # Display frames in separate windows
        cv2.imshow('Video 1', frame1)
        #cv2.imshow('Video 2', frame2)

        # Check for key press to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture objects and close OpenCV windows
    cap1.release()
    #cap2.release()
    cv2.destroyAllWindows()