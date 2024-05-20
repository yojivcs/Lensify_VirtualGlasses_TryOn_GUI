import os
import time
import dlib
import cv2
import numpy as np
import sqlite3
from scipy import ndimage
from pathlib import Path
from ctypes import windll
from tkinter import Tk, Canvas, Button, PhotoImage, Label, messagebox
from PIL import Image, ImageTk

# Set DPI awareness for high-resolution displays
windll.shcore.SetProcessDpiAwareness(1)

# Constants for video feed
VIDEO_WIDTH = 839
VIDEO_HEIGHT = 534

# Paths
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("assets/frame11")

# Utility function to manage asset paths
def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Function to resize an image to a certain width
def resize(img, width):
    r = float(width) / img.shape[1]
    dim = (width, int(img.shape[0] * r))
    img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    return img

# Function to blend images with transparency
def blend_transparent(face_img, sunglasses_img):
    overlay_img = sunglasses_img[:,:,:3]
    overlay_mask = sunglasses_img[:,:,3:]

    background_mask = 255 - overlay_mask

    overlay_mask = cv2.cvtColor(overlay_mask, cv2.COLOR_GRAY2BGR)
    background_mask = cv2.cvtColor(background_mask, cv2.COLOR_GRAY2BGR)

    face_part = (face_img * (1 / 255.0)) * (background_mask * (1 / 255.0))
    overlay_part = (overlay_img * (1 / 255.0)) * (overlay_mask * (1 / 255.0))

    return np.uint8(cv2.addWeighted(face_part, 255.0, overlay_part, 255.0, 0.0))

# Function to find the angle between two points
def angle_between(point_1, point_2):
    angle_1 = np.arctan2(*point_1[::-1])
    angle_2 = np.arctan2(*point_2[::-1])
    return np.rad2deg((angle_1 - angle_2) % (2 * np.pi))

# Initialize camera and load assets
video_capture = cv2.VideoCapture(0)

# Database connection
def get_glasses_image_path():
    conn = sqlite3.connect('glasses.db')
    cursor = conn.cursor()
    cursor.execute("SELECT path FROM glasses WHERE id = ?", (7,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    else:
        messagebox.showerror("Error", "No glasses found in the database.")
        return None

glasses_path = get_glasses_image_path()
if glasses_path:
    glasses = cv2.imread(glasses_path, -1)
else:
    glasses = None

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Create and configure the main window
window = Tk()
window.geometry("1920x980")
window.configure(bg = "#FFFFFF")

# Create and place the canvas
canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 980,
    width = 1920,
    bd = 0,
    highlightthickness= 0,
    relief = "ridge"
)
canvas.place(x = 0, y = 0)

# Load and place buttons and images
button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: capture_image(),
    relief="flat"
)
button_1.place(x=416.0, y=692.0, width=207.0, height=207.0)

image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
canvas.create_image(1371.0, 502.0, image=image_image_1)

image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
canvas.create_image(1371.0, 502.0, image=image_image_2)

canvas.create_text(1122.0, 503.0, anchor="nw", text="ANTILLE", fill="#FFFFFF", font=("Clash Display Semibold", 48 * -1))

image_image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
canvas.create_image(1541.0, 251.0, image=image_image_3)

image_image_4 = PhotoImage(file=relative_to_assets("image_4.png"))
canvas.create_image(1511.0, 282.0, image=image_image_4)

image_image_5 = PhotoImage(file=relative_to_assets("image_5.png"))
canvas.create_image(1831.0, 81.0, image=image_image_5)

canvas.create_text(1353.0, 599.0, anchor="nw", text="Antille\n", fill="#FFFFFF", font=("Clash Display Light", 36 * -1))

canvas.create_text(1122.0, 599.0, anchor="nw", text="Model Name: ", fill="#FFFFFF", font=("Clash Display Medium", 36 * -1))

canvas.create_text(1353.0, 645.0, anchor="nw", text="Net Black", fill="#FFFFFF", font=("Clash Display Light", 36 * -1))

canvas.create_text(1122.0, 645.0, anchor="nw", text="Frame Color: ", fill="#FFFFFF", font=("Clash Display Medium", 36 * -1))

canvas.create_text(1303.0, 695.0, anchor="nw", text="Wide", fill="#FFFFFF", font=("Clash Display Light", 36 * -1))

canvas.create_text(1122.0, 695.0, anchor="nw", text="Frame Fit: ", fill="#FFFFFF", font=("Clash Display Medium", 36 * -1))

canvas.create_text(1215.0, 741.0, anchor="nw", text="M", fill="#FFFFFF", font=("Clash Display Light", 36 * -1))

canvas.create_text(1122.0, 738.0, anchor="nw", text="Size:", fill="#FFFFFF", font=("Clash Display Medium", 36 * -1))

# Video label for webcam feed
video_label = Label(window)
video_label.place(x=100, y=126, width=VIDEO_WIDTH, height=VIDEO_HEIGHT)

# Function to capture and save an image
def capture_image():
    ret, frame = video_capture.read()
    if ret:
        frame = cv2.flip(frame, 1)  # Flip the frame to get the correct orientation
        frame = process_frame(frame)
        output_path = "button_capture"
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        image_path = os.path.join(output_path, f"capture_{int(time.time())}.png")
        cv2.imwrite(image_path, frame)
        print(f"Image saved to {image_path}")

# Function to process each frame (can be used for additional processing)
def process_frame(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
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

            for idx, point in enumerate(landmarks):
                pos = (point[0, 0], point[0, 1])
                if idx == 0:
                    eye_left = pos
                elif idx == 16:
                    eye_right = pos

            try:
                degree = np.rad2deg(np.arctan2(eye_left[0] - eye_right[0], eye_left[1] - eye_right[1]))
            except:
                pass

            eye_center = (eye_left[1] + eye_right[1]) / 2
            glass_trans = int(.2 * (eye_center - y))
            face_width = w - x
            glasses_resize = resize(glasses, face_width)

            yG, xG, cG = glasses_resize.shape
            glasses_resize_rotated = ndimage.rotate(glasses_resize, (degree + 90))
            glass_rec_rotated = ndimage.rotate(frame[y + glass_trans:y + yG + glass_trans, x:w], (degree + 90))

            h5, w5, s5 = glass_rec_rotated.shape
            rec_resize = frame[y + glass_trans:y + h5 + glass_trans, x:x + w5]
            blend_glass3 = blend_transparent(rec_resize, glasses_resize_rotated)
            frame[y + glass_trans:y + h5 + glass_trans, x:x + w5] = blend_glass3
    except:
        pass
    return frame

# Function to update video feed
def update_video():
    ret, img = video_capture.read()
    if ret:
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

                for idx, point in enumerate(landmarks):
                    pos = (point[0, 0], point[0, 1])
                    if idx == 0:
                        eye_left = pos
                    elif idx == 16:
                        eye_right = pos

                try:
                    degree = np.rad2deg(np.arctan2(eye_left[0] - eye_right[0], eye_left[1] - eye_right[1]))
                except:
                    pass

                eye_center = (eye_left[1] + eye_right[1]) / 2
                glass_trans = int(.2 * (eye_center - y))
                face_width = w - x
                glasses_resize = resize(glasses, face_width)

                yG, xG, cG = glasses_resize.shape
                glasses_resize_rotated = ndimage.rotate(glasses_resize, (degree + 90))
                glass_rec_rotated = ndimage.rotate(img[y + glass_trans:y + yG + glass_trans, x:w], (degree + 90))

                h5, w5, s5 = glass_rec_rotated.shape
                rec_resize = img_copy[y + glass_trans:y + h5 + glass_trans, x:x + w5]
                blend_glass3 = blend_transparent(rec_resize, glasses_resize_rotated)
                img_copy[y + glass_trans:y + h5 + glass_trans, x:x + w5] = blend_glass3
        except:
            pass

        img_copy = cv2.cvtColor(img_copy, cv2.COLOR_BGR2RGB)
        img_copy = Image.fromarray(img_copy)
        img_copy = ImageTk.PhotoImage(img_copy)
        video_label.configure(image=img_copy)
        video_label.image = img_copy

    video_label.after(10, update_video)

# Start video update loop
update_video()

# Run the application
window.resizable(False, False)
window.mainloop()

