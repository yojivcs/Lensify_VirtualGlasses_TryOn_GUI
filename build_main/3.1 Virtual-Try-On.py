from pathlib import Path
import cv2
import os
import time
import numpy as np
from scipy import ndimage
import sqlite3
import tkinter as tk
from PIL import Image, ImageTk
import dlib
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)
# Constants
VIDEO_WIDTH = 839
VIDEO_HEIGHT = 534
GLASSES_SCALE_FACTOR = 1.5
LEFT_EYE_INDEX = 36
RIGHT_EYE_INDEX = 45
NOSE_TIP_INDEX = 30


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("assets/frame3")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


class GlassesApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Virtual Glasses Try-On")
        self.geometry("1920x980")  # Fullscreen

        self.create_gui_elements()

        # Load the face detector and predictor
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

        # Connect to the database
        self.conn = sqlite3.connect('glasses.db')
        self.c = self.conn.cursor()

        # Get a list of all glasses in the database
        self.c.execute("SELECT * FROM glasses")
        self.glasses_list = self.c.fetchall()

        # Set the initial glass index to 2 as Mariana Trench is first
        self.glass_index = 2

        # Load the first glass
        self.glasses_path = self.glasses_list[self.glass_index][1]  # Get the path from the database
        self.glasses = cv2.imread(str(self.glasses_path), -1)

        self.video_capture = cv2.VideoCapture(0)

        self.update_video()

        # Bind keys
        self.bind('<KeyPress-n>', self.next_glasses)
        self.bind('<KeyPress-p>', self.prev_glasses)

    def create_gui_elements(self):
        canvas = tk.Canvas(
            self,
            bg="#FFFFFF",
            height=980,
            width=1920,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        canvas.place(x=0, y=0)

        image_image_1 = Image.open(relative_to_assets("image_1.png"))
        self.image_1 = ImageTk.PhotoImage(image_image_1)
        canvas.create_image(
            1831.0,
            81.0,
            image=self.image_1
        )

        button_image_1 = Image.open(relative_to_assets("button_1.png"))
        self.button_1 = ImageTk.PhotoImage(button_image_1)
        button_1 = tk.Button(
            image=self.button_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.apply_glasses(3),
            relief="flat"
        )
        button_1.place(
            x=1022.0,
            y=126.0,
            width=350.0,
            height=210
        )

        button_image_2 = Image.open(relative_to_assets("button_2.png"))
        self.button_2 = ImageTk.PhotoImage(button_image_2)
        button_2 = tk.Button(
            image=self.button_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.apply_glasses(8),
            relief="flat"
        )
        button_2.place(
            x=1022.0,
            y=385.0,
            width=350.0,
            height=210.0
        )

        button_image_3 = Image.open(relative_to_assets("button_3.png"))
        self.button_3 = ImageTk.PhotoImage(button_image_3)
        button_3 = tk.Button(
            image=self.button_3,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.apply_glasses(13),
            relief="flat"
        )
        button_3.place(
            x=1017.0,
            y=644.0,
            width=350.0,
            height=210.0
        )

        button_image_4 = Image.open(relative_to_assets("button_4.png"))
        self.button_4 = ImageTk.PhotoImage(button_image_4)
        button_image_4 = tk.Button(
            image=self.button_4,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.apply_glasses(15),
            relief="flat"
        )
        button_image_4.place(
            x=1402.0,
            y=385.0,
            width=350.0,
            height=210.0
        )

        button_image_5 = Image.open(relative_to_assets("button_5.png"))
        self.button_5 = ImageTk.PhotoImage(button_image_5)
        button_image_5 = tk.Button(
            image=self.button_5,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.apply_glasses(25),
            relief="flat"
        )
        button_image_5.place(
            x=1407.0,
            y=644.0,
            width=350.0,
            height=210.0
        )

        button_image_6 = Image.open(relative_to_assets("button_6.png"))
        self.button_6 = ImageTk.PhotoImage(button_image_6)
        button_image_6 = tk.Button(
            image=self.button_6,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.apply_glasses(2),
            relief="flat"
        )
        button_image_6.place(
            x=1402.0,
            y=126.0,
            width=350.0,
            height=210.0
        )

        button_image_7 = Image.open(relative_to_assets("button_7.png"))
        self.button_7 = ImageTk.PhotoImage(button_image_7)
        button_image_7 = tk.Button(
            image=self.button_7,
            borderwidth=0,
            highlightthickness=0,
            command=self.capture_image,
            relief="flat"
        )
        button_image_7.place(
            x=416.0,
            y=692.0,
            width=207.0,
            height=207.0
        )

    

        self.video_label = tk.Label(self)  # Create video label
        self.video_label.place(x=100, y=126, width=VIDEO_WIDTH, height=VIDEO_HEIGHT)  # Place video label

    def apply_glasses(self, id):
    # Find the glasses with the matching ID
        self.c.execute("SELECT * FROM glasses WHERE id=?", (id,))
        glasses = self.c.fetchone()
        print("Selected glasses:", glasses)  # Print the selected glasses for debugging
        if glasses:
            self.glasses_path = glasses[1]  # Update the path to the new glasses
            self.glasses = cv2.imread(str(self.glasses_path), -1)  # Load the new glasses image



    def next_glasses(self, event):
        self.glass_index = (self.glass_index + 1) % len(self.glasses_list)
        self.glasses_path = self.glasses_list[self.glass_index][1]  # Get the path from the database
        self.glasses = cv2.imread(str(self.glasses_path), -1)

    def prev_glasses(self, event):
        self.glass_index = (self.glass_index - 1) % len(self.glasses_list)
        self.glasses_path = self.glasses_list[self.glass_index][1]  # Get the path from the database
        self.glasses = cv2.imread(str(self.glasses_path), -1)
    
    def capture_image(self):
        ret, frame = self.video_capture.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = self.process_frame(frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            output_path = "button_capture"
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        image_path = os.path.join(output_path, f"capture_{int(time.time())}.png")
        cv2.imwrite(image_path, frame)
            

    def update_video(self):
        ret, frame = self.video_capture.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = self.process_frame(frame)
            frame = Image.fromarray(frame)
            frame = ImageTk.PhotoImage(frame)
            self.video_label.configure(image=frame)
            self.video_label.image = frame
        self.after(10, self.update_video)

    def process_frame(self, frame):
        frame = cv2.flip(frame, 1)
        frame = self.resize(frame, VIDEO_WIDTH)
        frame_copy = frame.copy()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        try:
            dets = self.detector(gray, 1)
            for d in dets:
                x = d.left()
                y = d.top()
                w = d.right()
                h = d.bottom()

                dlib_rect = dlib.rectangle(x, y, w, h)

                detected_landmarks = self.predictor(gray, dlib_rect).parts()
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
                    eye_angle = self.angle_between(eye_left, eye_right)
                    eye_midpoint = ((eye_left[0] + eye_right[0]) / 2, (eye_left[1] + eye_right[1]) / 2)
                    eye_distance = np.linalg.norm(np.array(eye_left) - np.array(eye_right))

                    glasses_resize = self.resize(self.glasses, int(eye_distance * GLASSES_SCALE_FACTOR))
                    glasses_resize_rotated = ndimage.rotate(glasses_resize, eye_angle)

                    yG, xG, cG = glasses_resize_rotated.shape
                    glass_trans_x = int(eye_midpoint[0] - xG / 2)
                    glass_trans_y = int(eye_midpoint[1] - yG / 2)

                    rec_resize = frame_copy[glass_trans_y:glass_trans_y + yG, glass_trans_x:glass_trans_x + xG]
                    blend_glass = self.blend_transparent(rec_resize, glasses_resize_rotated)
                    frame_copy[glass_trans_y:glass_trans_y + yG, glass_trans_x:glass_trans_x + xG] = blend_glass

        except Exception as e:
            print(f"Error processing frame: {e}")

        return frame_copy

    def resize(self, img, width):
        r = float(width) / img.shape[1]
        dim = (width, int(img.shape[0] * r))
        img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
        return img

    def blend_transparent(self, face_img, sunglasses_img):
        overlay_img = cv2.cvtColor(sunglasses_img, cv2.COLOR_BGR2RGB)[:,:,:3]
        overlay_mask = sunglasses_img[:,:,3:]

        background_mask = 255 - overlay_mask

        overlay_mask = cv2.cvtColor(overlay_mask, cv2.COLOR_GRAY2RGB)
        background_mask = cv2.cvtColor(background_mask, cv2.COLOR_GRAY2RGB)

        face_part = (face_img * (1 / 255.0)) * (background_mask * (1 / 255.0))
        overlay_part = (overlay_img * (1 / 255.0)) * (overlay_mask * (1 / 255.0))

        return np.uint8(cv2.addWeighted(face_part, 255.0, overlay_part, 255.0, 0.0))

    def angle_between(self, point_1, point_2):
        dx = point_2[0] - point_1[0]
        dy = point_2[1] - point_1[1]
        angle = np.degrees(np.arctan2(dy, dx))
        return angle


app = GlassesApp()
app.mainloop()