import tkinter as tk
from tkinter import messagebox
import cv2
import face_recognition
import time
import pyautogui
from scipy.spatial import distance
import pygame
from pyvidplayer2 import Video

# global vid
vid = Video("txt.mp4")
global duration_gone, alert_displayed, face_gone_time, closed_time, opened_time, closed_eyes_duration, open_eyes_duration

def reset_counter():
    global duration_gone, alert_displayed, face_gone_time, closed_time, opened_time, closed_eyes_duration, open_eyes_duration
    duration_gone = 0  # Timer to track how long the face is not detected
    alert_displayed = False  # Flag to track if alert message is displayed
    face_gone_time = -1
    closed_time = -1
    opened_time = -1
    closed_eyes_duration = 0
    open_eyes_duration = 0

def show_alert(type, blink):
    root = tk.Tk() 
    root.attributes("-topmost", True)  # Ensure the alert window is on top
    root.withdraw()  # Hide the tkinter window
    vid.toggle_pause()
    reset_counter()
    if type == 'face':
        tk.messagebox.showwarning("Face Not Detected ", "Face not detected for more than 5 seconds!")
    elif type == 'eye':
        tk.messagebox.showwarning("Blink Not Detected ", "Blink not detected for more than " + str(blink) + " seconds!")
    vid.toggle_pause()
    root.destroy()  # Destroy the tkinter window after showing the alert
    # Freeze the screen
    # pyautogui.press('space')

def draw_landmarks(frame, landmarks):
    for landmark_type in landmarks:
        for point in landmarks[landmark_type]:
            cv2.circle(frame, point, 2, (0, 0, 255), -1)

def detect_blink(landmarks):
    # Assuming left eye landmarks are at index 0 and right eye landmarks are at index 1
    left_eye = landmarks['left_eye']
    right_eye = landmarks['right_eye']

    # Calculate the aspect ratio of the eyes
    left_eye_aspect_ratio = eye_aspect_ratio(left_eye)
    right_eye_aspect_ratio = eye_aspect_ratio(right_eye)

    # Average the aspect ratios of both eyes
    avg_eye_aspect_ratio = (left_eye_aspect_ratio + right_eye_aspect_ratio) / 2.0

    return avg_eye_aspect_ratio

def eye_aspect_ratio(eye):
    # Compute the euclidean distances between the two sets of vertical eye landmarks
    a = distance.euclidean(eye[1], eye[5])
    b = distance.euclidean(eye[2], eye[4])

    # Compute the euclidean distance between the horizontal eye landmarks
    c = distance.euclidean(eye[0], eye[3])

    # Compute the eye aspect ratio
    ear = (a + b) / (2.0 * c)
    return ear

def init():
    cap = cv2.VideoCapture(0)
    global duration_gone, alert_displayed, face_gone_time, closed_time, opened_time, closed_eyes_duration, open_eyes_duration

    reset_counter()

    win = pygame.display.set_mode(vid.current_size)
    pygame.display.set_caption(vid.name)

    while vid.active:

        key = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                vid.stop()
            elif event.type == pygame.KEYDOWN:
                key = pygame.key.name(event.key)

        if key == "q":
            vid.stop()
        if key == "r":
            vid.restart()           #rewind video to beginning
        elif key == "p":
            vid.toggle_pause()      #pause/plays video
            reset_counter()
        elif key == "m":
            vid.toggle_mute()       #mutes/unmutes video
        elif key == "right":
            vid.seek(15)            #skip 15 seconds in video
        elif key == "left":
            vid.seek(-15)           #rewind 15 seconds in video
        elif key == "up":
            vid.set_volume(1.0)     #max volume
        elif key == "down":
            vid.set_volume(0.0)     #min volume
        elif key == "1":
            vid.set_speed(1.0)      #regular playback speed
        elif key == "2":
            vid.set_speed(2.0)      #doubles video speed

        start_time = time.time()  # Start time of the loop iteration

        # Capture frame-by-frame
        ret, frame = cap.read()

        rgb_frame = frame[:, :, ::-1]
        # Find all the faces in the current frame of video
        face_locations = face_recognition.face_locations(rgb_frame)
        face_landmarks = face_recognition.face_landmarks(rgb_frame)

        if not vid.get_paused():

            if (face_locations or alert_displayed):
                # Reset the timer if face is detected
                duration_gone = 0
                face_gone_time = -1
                alert_displayed = False

                for landmarks in face_landmarks:
                    draw_landmarks(frame, landmarks)

                    ear = detect_blink(landmarks)
                    
                    if ear < 0.3:  # Assuming 0.2 as the threshold for blink detection
                        # Increment the closed eyes timer
                        if closed_eyes_duration == 0:
                            closed_time = time.time()
                        closed_eyes_duration += 1
                        # Reset the open eyes timer
                        open_eyes_duration = 0
                        opened_time = -1
                    else:
                        # Reset the closed eyes timer
                        if open_eyes_duration == 0:
                            opened_time = time.time()
                        closed_eyes_duration = 0
                        closed_time = -1
                        # Increment the open eyes timer
                        open_eyes_duration += 1
            else:
                # Increment the timer if face is not detected
                if duration_gone == 0:
                    face_gone_time = time.time()
                duration_gone += 1

            curr_time = time.time()
            face_elapsed_time = 0
            close_elapsed_time = 0
            open_elapsed_time = 0

            if face_gone_time >= 0:
                face_elapsed_time = curr_time - face_gone_time
            elif closed_time >= 0:
                close_elapsed_time = curr_time - closed_time
            elif opened_time >= 0:
                open_elapsed_time = curr_time - opened_time

            # Display alert message if face is not detected for more than 5 seconds
            if not alert_displayed:
                # print("face ", face_elapsed_time)
                # print("closed ", close_elapsed_time)
                # print("opened ", open_elapsed_time)

                if face_elapsed_time >= 5:
                    show_alert('face', 0)
                    alert_displayed = True
                if face_locations:
                    if open_eyes_duration == 0 and close_elapsed_time >= 5:
                        show_alert('eye', 5)
                        alert_displayed = True
                        closed_time = -1
                        opened_time = -1
                        closed_eyes_duration = 0
                        open_eyes_duration = 0
                    elif closed_eyes_duration == 0 and open_elapsed_time >= 10:
                        show_alert('eye', 10)
                        alert_displayed = True
                        closed_time = -1
                        opened_time = -1
                        closed_eyes_duration = 0
                        open_eyes_duration = 0            
        else:
            reset_counter()

        # Display the resulting image
        cv2.imshow('Video', frame)

        # only draw new frames, and only update the screen if something is drawn
        if vid.draw(win, (0, 0), force_draw=False):
            pygame.display.update()

        # pygame.time.wait(30) # around 60 fps

        """
        # Calculate the time taken for the loop iteration
        iteration_time = time.time() - start_time

        # Introduce a delay to control frame rate
        if iteration_time < 0.04:  # Adjust the value as needed for desired frame rate
            time.sleep(0.04 - iteration_time)

        """
        
# I want to make it so that the video only counts the seconds if the video is playing
# If the video is paused, it would reset the count for whatever reason and not count
# If the vidoe is playing, it would do the normal thing

    # close face detection when done
    cap.release()
    cv2.destroyAllWindows()

    # close video when done
    vid.close()
    pygame.quit()

init()