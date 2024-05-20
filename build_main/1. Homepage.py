from pathlib import Path
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)
from tkinter import Tk, Canvas, Button, PhotoImage
import subprocess
import sys

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("assets/frame1")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def open_about_us():
    about_us_script = OUTPUT_PATH / "2. AboutUs.py"
    subprocess.Popen([sys.executable, str(about_us_script)])
    window.destroy()


window = Tk()

window.geometry("1920x980")
window.configure(bg="#FFFFFF")

canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=980,
    width=1920,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)
canvas.create_text(
    1101.66357421875,
    230.51123046875,
    anchor="nw",
    text="Welcome To\nLensify !!",
    fill="#231A49",
    font=("Montserrat ExtraBold", 105 * -1)
)

canvas.create_text(
    1101.66357421875,
    525.933349609375,
    anchor="nw",
    text="Try on Your Vision, Virtually.",
    fill="#5E89CE",
    font=("Clash Display Medium", 36 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=open_about_us,  # Changed command to open About Us page
    relief="flat"
)
button_1.place(
    x=1104.0,
    y=605.111083984375,
    width=487.43756103515625,
    height=120.888916015625
)

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    1045.0,
    641.300048828125,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    911.19677734375,
    581.895263671875,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    529.0,
    476.0,
    image=image_image_3
)

window.resizable(False, False)
window.mainloop()
