import cv2
import os
import dlib

# Open the default camera (index 0)
cap = cv2.VideoCapture(0)

# Load the face detector and facial landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

while True:
    # Read a frame from the camera
    ret, frame = cap.read()
    
    # Flip the frame horizontally
    frame = cv2.flip(frame, 1)
    
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect faces in the grayscale image
    faces = detector(gray, 0)
    
    # Draw rectangles around the detected faces
    for face in faces:
        x, y = face.left(), face.top()
        xw, yh = face.right(), face.bottom()
        cv2.rectangle(frame, (x, y), (xw, yh), (0, 255, 0), 2)
        
        # Detect facial landmarks
        landmarks = predictor(gray, face)
        
        # Draw landmarks on the image
        for n in range(0, 68):
            x = landmarks.part(n).x
            y = landmarks.part(n).y
            cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)
    
    # Display the output
    cv2.imshow('frame', frame)
    
    # Check for the 'c' key to capture an image
    if cv2.waitKey(1) & 0xFF == ord('c'):
        # Save the image to a directory
        img_path = 'captured_images/image_{}.jpg'.format(len(os.listdir('captured_images')))
        cv2.imwrite(img_path, frame)
        print('Image saved to {}'.format(img_path))
    
    # Check for the 'q' key to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the window
cap.release()
cv2.destroyAllWindows()