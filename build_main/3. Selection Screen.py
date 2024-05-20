
from pathlib import Path
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import sys 
import subprocess

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("assets/frame2")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def open_virtualtryon():
    selection_script = OUTPUT_PATH / "3.1 Virtual-Try-On.py"
    subprocess.Popen([sys.executable, str(selection_script)])

def open_glasses():
    selection_script = OUTPUT_PATH / "3.2 Glasses Catalogue.py"
    subprocess.Popen([sys.executable, str(selection_script)])
    

def open_sunglasses():
    selection_script = OUTPUT_PATH / "3.3 Sunglasses Catalogue.py"
    subprocess.Popen([sys.executable, str(selection_script)])
    

window = Tk()

window.geometry("1920x980")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 980,
    width = 1920,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    1359.0,
    708.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    1359.0,
    818.0,
    image=image_image_2
)

canvas.create_text(
    1076.0,
    776.0,
    anchor="nw",
    text="Browse Sunglasses",
    fill="#FFFFFF",
    font=("Montserrat Bold", 32 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=open_sunglasses,
    relief="flat"
)
button_1.place(
    x=1076.0,
    y=824.0,
    width=212.0,
    height=50.0
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    1359.0,
    328.0,
    image=image_image_3
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    1359.0,
    425.0,
    image=image_image_4
)

canvas.create_text(
    1076.0,
    383.0,
    anchor="nw",
    text="Browse Glasses",
    fill="#FFFFFF",
    font=("Montserrat Bold", 32 * -1)
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=open_glasses,
    relief="flat"
)
button_2.place(
    x=1076.0,
    y=433.0,
    width=212.0,
    height=50.0
)

canvas.create_rectangle(
    186.0,
    151.0,
    985.0,
    895.0,
    fill="#231A49",
    outline="")

image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(
    599.0,
    524.0,
    image=image_image_5
)

image_image_6 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(
    577.0,
    776.0,
    image=image_image_6
)

canvas.create_text(
    240.0,
    724.0,
    anchor="nw",
    text="Virtual-Try-On",
    fill="#FFFFFF",
    font=("Montserrat Bold", 48 * -1)
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=open_virtualtryon,
    relief="flat"
)
button_3.place(
    x=240.0,
    y=798.0,
    width=219.0,
    height=50.0
)

image_image_7 = PhotoImage(
    file=relative_to_assets("image_7.png"))
image_7 = canvas.create_image(
    97.9248046875,
    83.94384765625,
    image=image_image_7
)
window.resizable(False, False)
window.mainloop()
