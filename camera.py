import cv2
import face_recognition

def init():
    cap = cv2.VideoCapture(0)

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        rgb_frame = frame[:, :, ::-1]
        # Find all the faces in the current frame of video
        face_locations = face_recognition.face_locations(rgb_frame)

        for top, right, bottom, left in face_locations:
            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0,  
            255), 2)
        # Display the resulting image
        cv2.imshow('Video', frame)

        if cv2.waitKey(25) == 13:
            break

    cap.release()
    cv2.destroyAllWindows()

init()
