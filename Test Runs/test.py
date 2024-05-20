#!/usr/bin/python
import os
import dlib
import cv2
import numpy as np
from scipy import ndimage
import sqlite3


# Constants
VIDEO_WIDTH = 700
GLASSES_SCALE_FACTOR = 1.5
LEFT_EYE_INDEX = 36
RIGHT_EYE_INDEX = 45
NOSE_TIP_INDEX = 30

# Connect to the database
conn = sqlite3.connect('glasses.db')
c = conn.cursor()

# Get a list of all glasses in the database
c.execute("SELECT * FROM glasses")
glasses_list = c.fetchall()

# Set the initial glass index to 0
glass_index = 0

# Initialize the video capture object
video_capture = cv2.VideoCapture(0)

# Load the face detector and predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Load the first glass
glasses_path = glasses_list[glass_index][1]  # Get the path from the database
glasses = cv2.imread(glasses_path, -1)

def resize(img, width):
    r = float(width) / img.shape[1]
    dim = (width, int(img.shape[0] * r))
    img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    return img

def blend_transparent(face_img, sunglasses_img):
    overlay_img = sunglasses_img[:,:,:3]
    overlay_mask = sunglasses_img[:,:,3:]
    
    background_mask = 255 - overlay_mask

    overlay_mask = cv2.cvtColor(overlay_mask, cv2.COLOR_GRAY2BGR)
    background_mask = cv2.cvtColor(background_mask, cv2.COLOR_GRAY2BGR)

    face_part = (face_img * (1 / 255.0)) * (background_mask * (1 / 255.0))
    overlay_part = (overlay_img * (1 / 255.0)) * (overlay_mask * (1 / 255.0))

    return np.uint8(cv2.addWeighted(face_part, 255.0, overlay_part, 255.0, 0.0))

def angle_between(point_1, point_2):
    dx = point_2[0] - point_1[0]
    dy = point_2[1] - point_1[1]
    angle = np.degrees(np.arctan2(dy, dx))
    return angle

def process_frame(img):
    img = cv2.flip(img, 1)
    img = resize(img, VIDEO_WIDTH)
    img_copy = img.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    try:
        dets = detector(gray, 1)
        for d in dets:
            x = d.left()
            y = d.top()
            w = d.right()
            h = d.bottom()

            dlib_rect = dlib.rectangle(x, y, w, h)

            detected_landmarks = predictor(gray, dlib_rect).parts()
            landmarks = np.matrix([[p.x, p.y] for p in detected_landmarks])

            eye_left = eye_right = nose_tip = None
            for idx, point in enumerate(landmarks):
                pos = (point[0, 0], point[0, 1])
                if idx == LEFT_EYE_INDEX:
                    eye_left = pos
                elif idx == RIGHT_EYE_INDEX:
                    eye_right = pos
                elif idx == NOSE_TIP_INDEX:
                    nose_tip = pos

            if eye_left and eye_right:
                eye_angle = angle_between(eye_left, eye_right)
                eye_midpoint = ((eye_left[0] + eye_right[0]) / 2, (eye_left[1] + eye_right[1]) / 2)
                eye_distance = np.linalg.norm(np.array(eye_left) - np.array(eye_right))

                glasses_resize = resize(glasses, int(eye_distance * GLASSES_SCALE_FACTOR))
                glasses_resize_rotated = ndimage.rotate(glasses_resize, eye_angle)

                yG, xG, cG = glasses_resize_rotated.shape
                glass_trans_x = int(eye_midpoint[0] - xG / 2)
                glass_trans_y = int(eye_midpoint[1] - yG / 2)

                rec_resize = img_copy[glass_trans_y:glass_trans_y + yG, glass_trans_x:glass_trans_x + xG]
                blend_glass3 = blend_transparent(rec_resize, glasses_resize_rotated)
                img_copy[glass_trans_y:glass_trans_y + yG, glass_trans_x:glass_trans_x + xG] = blend_glass3

    except Exception as e:
        print(f"Error processing frame: {e}")

    return img_copy

while True:
    ret, img = video_capture.read()
    if not ret:
        break

    img_copy = process_frame(img)
    cv2.imshow('Output', img_copy)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('n'):
        glass_index = (glass_index + 1) % len(glasses_list)
        glasses_path = glasses_list[glass_index][1]  # Get the path from the database
        glasses = cv2.imread(glasses_path, -1)
    elif key == ord('p'):
        glass_index = (glass_index - 1) % len(glasses_list)
        glasses_path = glasses_list[glass_index][1]  # Get the path from the database
        glasses = cv2.imread(glasses_path, -1)

video_capture.release()
cv2.destroyAllWindows()
conn.close()
