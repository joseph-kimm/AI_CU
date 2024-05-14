import cv2
import face_recognition
import time
import tkinter as tk
from tkinter import messagebox
from moviepy.editor import VideoFileClip
import time
import pygame
from pyvidplayer2 import Video

def playVideo1():

    video_path = "nba.mp4"

    pygame.init()
    pygame.display.set_caption(video_path)
    # Define the video file path
    

    # Load the video clip
    clip = VideoFileClip(video_path)

    # Play the video
    clip = clip.subclip(0, 10) 
    clip.preview(fps= 60)  # This will start playing the vide
    pygame.quit()


def playVideo2():

    # create video object

    vid = Video("nba.mp4")

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

        # only draw new frames, and only update the screen if something is drawn
        
        if vid.draw(win, (0, 0), force_draw=False):
            pygame.display.update()

        pygame.time.wait(16) # around 60 fps

    # close video when done

    vid.close()
    pygame.quit()


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

playVideo2()