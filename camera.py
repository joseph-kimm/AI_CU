import tkinter as tk
import cv2
import face_recognition
import time
from scipy.spatial import distance
import pygame
from pyvidplayer2 import Video
import platform
from tkinter import messagebox
import WebCamVideo
import imutils

# Try importing AppKit for macOS functionality (if available)
try:
  if platform.system() == "Darwin":  # Check for macOS using platform module
    from AppKit import NSApplication, NSAlert, NSWindow
except ModuleNotFoundError:
  pass

# global vid
vid = Video("txt.mp4")
global face_gone_time, closed_time, opened_time, gone_duration, closed_eyes_duration, open_eyes_duration

def reset_counter():
    global face_gone_time, closed_time, opened_time, gone_duration, closed_eyes_duration, open_eyes_duration
    face_gone_time = -1
    closed_time = -1
    opened_time = -1
    gone_duration = 0  # Timer to track how long the face is not detected
    closed_eyes_duration = 0 # Timer to track how long eyes are closed for
    open_eyes_duration = 0 # Timer to track how long eyes are open for

# showing alert
def show_alert(type, blink):

    os_name = platform.system()

    # Check if the program is running on macOS
    if os_name == 'Darwin':

        vid.toggle_pause()

        alert = NSAlert.alloc().init()
        alert.setMessageText_("Alert!")

        if type == 'face':
            alert.setInformativeText_("Face not detected for more than 5 seconds!")

        elif type == 'eye':
            alert.setInformativeText_("Blink not detected for more than " + str(blink) + " seconds!")
        
        response = alert.runModal()
        vid.toggle_pause()

    # Check if the program is running on Windows
    elif os_name == 'Windows':
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


# drawing points in face
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

def video_control(key):
    if key == "q":
            vid.stop()
    elif key == "r":
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

def init():

    # getting face image from camera
    cap = WebCamVideo.WebcamVideoStream(src=0).start()

    global face_gone_time, closed_time, opened_time, gone_duration, closed_eyes_duration, open_eyes_duration

    # reset all the counters that we havey
    reset_counter()

    # setting display for the educatinal video
    win = pygame.display.set_mode(vid.current_size)
    pygame.display.set_caption(vid.name)

    # while there is a video
    while vid.active:

        # detecting any keys taht are pressed
        key = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                vid.stop()
            elif event.type == pygame.KEYDOWN:
                key = pygame.key.name(event.key)

        # if a key has been pressed
        if key: 
            video_control(key)

        # Capture frame-by-frame
        frame = cap.read()

        # reducing size and changing into grayscale for efficiency
        frame = imutils.resize(frame, width=400)
        grayscale_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        # Find all the faces and features in the current frame of video
        face_locations = face_recognition.face_locations(frame)
        face_landmarks = face_recognition.face_landmarks(frame)

        # if video is playing right now
        if not vid.get_paused():

            # if face detected 
            if face_locations:
                
                # reset 
                gone_duration = 0
                face_gone_time = -1

                for landmarks in face_landmarks:

                    # commented it out as we don't actually have to draw anything lol
                    draw_landmarks(frame, landmarks)

                    ear = detect_blink(landmarks)
                    
                    if ear < 0.25:  # Assuming 0.2 as the threshold for blink detection
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

            # face is not detected
            else:
                # Increment the timer if face is not detected
                if gone_duration == 0:
                    face_gone_time = time.time()
                gone_duration += 1

            # finding time diff between curr and last time an event has occurred
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


            alert = False

            # if any of events are beyond timing we have set, show alert
            if face_elapsed_time >= 5:
                show_alert('face', 0)
                alert = True

            if face_locations:
                if open_eyes_duration == 0 and close_elapsed_time >= 5:
                    show_alert('eye', 5)
                    alert = True

                elif closed_eyes_duration == 0 and open_elapsed_time >= 20:
                    show_alert('eye', 20)
                    alert = True

            # if alert has been shown, reset all counter
            if alert:
                reset_counter()    

        # if video is paused, reset all counter
        else:
            reset_counter()

        # Display the resulting image
        cv2.imshow('Video', frame)

        # only draw new frames, and only update the screen if something is drawn
        if vid.draw(win, (0, 0), force_draw=False):
            pygame.display.update()

        #pygame.time.wait(16) # around 60 fps

    # close face detection when done
    cap.stop()
    cv2.destroyAllWindows()

    # close video when done
    vid.close()
    pygame.quit()

init()