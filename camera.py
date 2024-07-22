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
from pymongo import MongoClient

# Try importing AppKit for macOS functionality (if available)
try:
  if platform.system() == "Darwin":  # Check for macOS using platform module
    from AppKit import NSApplication, NSAlert, NSWindow
except ModuleNotFoundError:
  pass

# global vid
vid = Video("ani.mp4")
global gone_timestamp, closed_timestamp, face_gone, face_closed, gone_alarm_duration, closed_alarm_duration, \
      gone_alarm_count, closed_alarm_count, pause_duration, duration_limit, paused_timestamp, resume_timestamp

def initial_values():
    global gone_timestamp, closed_timestamp, face_gone, face_closed, gone_alarm_duration, closed_alarm_duration, \
        gone_alarm_count, closed_alarm_count, pause_duration, duration_limit
    
    gone_timestamp = -1
    closed_timestamp = -1

    gone_alarm_duration = 0
    closed_alarm_duration = 0
    gone_alarm_count = 0
    closed_alarm_count = 0
    pause_duration = 0
    face_gone = False
    face_closed = False

    # setting the limit of learning time
    duration_limit = 1 *60


def reset_counter():
    global gone_timestamp, closed_timestamp, face_gone, face_closed
    gone_timestamp = -1
    closed_timestamp = -1

    face_gone = False
    face_closed = False

# showing alert
def show_alert(type, blink):
    global gone_alarm_duration, closed_alarm_duration, gone_alarm_count, closed_alarm_count

    os_name = platform.system()

    vid.toggle_pause()
    alarm_timestamp = time.time()

    # if computer is running on MacOS
    if os_name == 'Darwin':
        alert = NSAlert.alloc().init()
        alert.setMessageText_("Alert!")

        if type == 'face':
            alert.setInformativeText_("Face not detected for more than 5 seconds!")

        elif type == 'eye':
            alert.setInformativeText_("Eyes closed for more than " + str(blink) + " seconds!")
        
        response = alert.runModal()

    # if computer is running on Windows
    elif os_name == 'Windows':
        root = tk.Tk() 
        root.attributes("-topmost", True)  # Ensure the alert window is on top
        root.withdraw()  # Hide the tkinter window

        if type == 'face':
            tk.messagebox.showwarning("Face Not Detected ", "Face not detected for more than 5 seconds!")
        elif type == 'eye':
            tk.messagebox.showwarning("Eyes closed ", "Eyes closed for more than " + str(blink) + " seconds!")

        root.destroy()
    
    vid.toggle_pause()
    
    if type == 'face':
        gone_alarm_duration += time.time() - alarm_timestamp
        gone_alarm_count += 1
    
    elif type == 'eye':
        closed_alarm_duration += time.time() - alarm_timestamp
        closed_alarm_count += 1

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

    global pause_duration, paused_timestamp, resume_timestamp

    if key == "q":
            vid.stop()
              
    elif key == "space":
        vid.toggle_pause()      #pause/plays video

        # records timestamp of when it was paused
        if vid.paused:
            paused_timestamp = time.time()
        
        # records timestamp of when it was resumed
        # adds the total time video was paused to pause_duration
        else:
            resume_timestamp = time.time()
            pause_duration += resume_timestamp - paused_timestamp

        reset_counter()
    elif key == "left":
        vid.seek(-15)           #rewind 15 seconds in video

    # keys that are not required for the program
    """
    elif key == "r":            #rewind video to beginning
        vid.restart() 
    elif key == "right":
        vid.seek(15)            #skip 15 seconds in video
    elif key == "m":
        vid.toggle_mute()       #mutes/unmutes video
    """

def display_link():
    return

def save_to_db(data):
    # Connect to MongoDB (Replace <username>, <password>, and <cluster-url> with your MongoDB credentials)
    client = MongoClient("mongodb+srv://eunclar:RLAskawn123!@mongocluster.g3klhii.mongodb.net/")
    db = client['user_data']
    collection = db['video_data']
    
    # Insert the data into the collection
    collection.insert_one(data)

def init():
    # getting face image from camera
    cap = WebCamVideo.WebcamVideoStream(src=0).start()

    global gone_timestamp, closed_timestamp, face_gone, face_closed, gone_alarm_duration, closed_alarm_duration, \
          gone_alarm_count, closed_alarm_count, pause_duration, duration_limit

    # reset all the counters that we have
    initial_values()

    # setting display for the educatinal video
    win = pygame.display.set_mode(vid.current_size)
    pygame.display.set_caption(vid.name)

    start_time = time.time()

    # while there is a video
    while vid.active:

        # detecting any keys that are pressed
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

            curr_time = time.time()
            if curr_time - start_time - pause_duration - gone_alarm_duration - closed_alarm_duration >= duration_limit:
                print(vid.get_pos())
                vid.stop()

            # if face detected 
            if face_locations:
                
                # reset
                face_gone = False
                gone_timestamp = -1

                for landmarks in face_landmarks:

                    # commented it out as we don't actually have to draw anything lol
                    draw_landmarks(frame, landmarks)

                    ear = detect_blink(landmarks)
                    
                    # eyes closed
                    if ear < 0.25:  # Assuming 0.2 as the threshold for blink detection

                        # set time stamp if eyes closed for the first time
                        if not face_closed:
                            closed_timestamp = time.time()
                        face_closed = True

                    # eyes open
                    else:
                        face_closed = False
                        closed_timestamp = -1

            # face is not detected
            else:

                # set time stamp if face_gone for the first time
                if not face_gone:
                    gone_timestamp = time.time()
                face_gone = True

            # finding time diff between curr and last time an event has occurred
            curr_time = time.time()

            # if face was gone for more than 5 seconds
            if gone_timestamp >= 0 and curr_time - gone_timestamp >= 5: 
                show_alert('face', 0)
                reset_counter()

            if closed_timestamp >= 0 and curr_time - closed_timestamp >= 5:
                show_alert('eye', 5)
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

    data = {
        "closed_alarm_count": closed_alarm_count,
        "closed_alarm_duration": closed_alarm_duration,
        "gone_alarm_count": gone_alarm_count,
        "gone_alarm_duration": gone_alarm_duration,
        "pause_duration": pause_duration
    }
    save_to_db(data)

init()
print(closed_alarm_count)
print(closed_alarm_duration)
print(gone_alarm_count)
print(gone_alarm_duration)
print(pause_duration)