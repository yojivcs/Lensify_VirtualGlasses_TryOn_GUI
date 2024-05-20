
from pathlib import Path
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import subprocess
import sys


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("assets/frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def open_selection_screen():
    selection_script = OUTPUT_PATH / "3. Selection Screen.py"
    subprocess.Popen([sys.executable, str(selection_script)])
    window.destroy()

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
    276.13232421875,
    375.35791015625,
    image=image_image_1
)

canvas.create_text(
    185.0,
    307.0,
    anchor="nw",
    text="Lensify is a ground-breaking\nsoftware program that is intended\nto completely change how people\nbrowse and choose glasses\nand sunglasses. Lensify's cutting-edge\nvirtual try-on function lets\ncustomers see and try on different\neyewear options in real time.",
    fill="#5E89CE",
    font=("Clash Display Medium", 48 * -1)
)

canvas.create_text(
    185.0,
    151.0,
    anchor="nw",
    text="About Us",
    fill="#231A49",
    font=("Montserrat ExtraBold", 95 * -1)
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    97.925048828125,
    83.94384765625,
    image=image_image_2
)

canvas.create_rectangle(
    1212.0,
    163.0,
    1743.0,
    816.0,
    fill="#FFFFFF",
    outline="#231A49",
    width = 15
    )

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=open_selection_screen,
    relief="flat"
)
button_1.place(
    x=1394.0,
    y=773.0,
    width=159.0,
    height=103.47900390625
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    1444.643798828125,
    518.14697265625,
    image=image_image_3
)
window.resizable(False, False)
window.mainloop()
