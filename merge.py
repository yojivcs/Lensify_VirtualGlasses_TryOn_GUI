from tkinter import Tk, Canvas, Button, PhotoImage
from pathlib import Path
from ctypes import windll
import cv2
from PIL import Image, ImageTk
import dlib
import numpy as np
from scipy import ndimage
import sqlite3

# Set DPI awareness
windll.shcore.SetProcessDpiAwareness(1)

# Constants for webcam feed
VIDEO_WIDTH = 700
GLASSES_SCALE_FACTOR = 1.5
LEFT_EYE_INDEX = 36
RIGHT_EYE_INDEX = 45
NOSE_TIP_INDEX = 30

# Constants for GUI
GUI_WIDTH = 1920
GUI_HEIGHT = 980
CAMERA_WIDTH = 839
CAMERA_HEIGHT = 534
CAMERA_X = 100
CAMERA_Y = 86

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
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

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

def update_camera(canvas):
    ret, frame = video_capture.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = resize(frame, CAMERA_WIDTH)
        photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
        canvas.create_image(CAMERA_X, CAMERA_Y, image=photo, anchor='nw')
        canvas.photo = photo
    canvas.after(15, update_camera, canvas)

# Create GUI window
window = Tk()
window.geometry(f"{GUI_WIDTH}x{GUI_HEIGHT}")
window.configure(bg="#FFFFFF")

# Create canvas for webcam feed and buttons
canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=GUI_HEIGHT,
    width=GUI_WIDTH,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)

# Load GUI assets
image_1 = PhotoImage(file="image_1.png")
button_1 = Button(
    image=PhotoImage(file="button_1.png"),
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_2 = Button(
    image=PhotoImage(file="button_2.png"),
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_3 = Button(
    image=PhotoImage(file="button_3.png"),
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_3 clicked"),
    relief="flat"
)

# Place GUI assets
canvas.create_image(1831.0, 81.0, image=image_1)
button_1.place(x=1071.8494873046875, y=301.0)
button_2.place(x=1071.8494873046875, y=71.0)
button_3.place(x=416.0, y=692.0)

# Add Virtual-Try-On text
canvas.create_text(
    1491.2750244140625,
    852.1999154585673,
    anchor="nw",
    text="Virtual-Try-On",
    fill="#FFFFFF",
    font=("ClashDisplay Semibold", 37 * -1)
)

# Update webcam feed in canvas
update_camera(canvas)

# Run GUI window
window.mainloop()

# Release resources
video_capture.release()
cv2.destroyAllWindows()
conn.close()
