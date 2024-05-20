
from pathlib import Path
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import subprocess
import sys

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("assets/frame5")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def open_grandcatalina():
    selection_script = OUTPUT_PATH / "3.3.1 Grand Catalina.py"
    subprocess.Popen([sys.executable, str(selection_script)])

def open_antille():
    selection_script = OUTPUT_PATH / "3.3.2 Antille.py"
    subprocess.Popen([sys.executable, str(selection_script)])

def open_tailfin():
    selection_script = OUTPUT_PATH / "3.3.3 Tailfin.py"
    subprocess.Popen([sys.executable, str(selection_script)])

def open_catherine():
    selection_script = OUTPUT_PATH / "3.3.4 Catherine.py"
    subprocess.Popen([sys.executable, str(selection_script)])

def open_gannet():
    selection_script = OUTPUT_PATH / "3.3.5 Gannet.py"
    subprocess.Popen([sys.executable, str(selection_script)])  

def open_nusa():
    selection_script = OUTPUT_PATH / "3.3.6 Nusa.py"
    subprocess.Popen([sys.executable, str(selection_script)]) 

def open_waterwoman():
    selection_script = OUTPUT_PATH / "3.3.7 Waterwoman.py"
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
button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=open_waterwoman,
    relief="flat"
)
button_1.place(
    x=1450.0,
    y=701.0,
    width=357.9864196777344,
    height=163.92010498046875
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=1026.0,
    y=698.0,
    width=361.7547302246094,
    height=167.06031799316406
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=open_nusa,
    relief="flat"
)

button_3.place(
    x=593.0,
    y=689.0,
    width=358.0,
    height=176.0
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=open_gannet,
    relief="flat"
)
button_4.place(
    x=176.0,
    y=689.0,
    width=356.1023254394531,
    height=168.31646728515625
)

button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=open_catherine,
    relief="flat"
)
button_5.place(
    x=1450.0,
    y=396.0,
    width=353.4664611816406,
    height=161.0
)

button_image_6 = PhotoImage(
    file=relative_to_assets("button_6.png"))
button_6 = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    command=open_tailfin,
    relief="flat"
)
button_6.place(
    x=1007.0,
    y=400.0,
    width=355.0,
    height=161.0
)

button_image_7 = PhotoImage(
    file=relative_to_assets("button_7.png"))
button_7 = Button(
    image=button_image_7,
    borderwidth=0,
    highlightthickness=0,
    command=open_antille,
    relief="flat"
)
button_7.place(
    x=580.0,
    y=395.0,
    width=354.2181396484375,
    height=161.4079132080078
)

button_image_8 = PhotoImage(
    file=relative_to_assets("button_8.png"))
button_8 = Button(
    image=button_image_8,
    borderwidth=0,
    highlightthickness=0,
    command=open_grandcatalina,
    relief="flat"
)
button_8.place(
    x=175.0,
    y=380.0,
    width=355.0,
    height=174.0
)

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    960.0,
    142.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    1826.0,
    75.0,
    image=image_image_2
)

canvas.create_text(
    106.0,
    30.0,
    anchor="nw",
    text="The Glasses You Want, \nThe Vision You Deserve",
    fill="#FFFFFF",
    font=("Montserrat Bold", 64 * -1)
)

canvas.create_text(
    110.0,
    225.0,
    anchor="nw",
    text="Discover the Perfect Eye Glasses for Men and Women",
    fill="#FFFFFF",
    font=("Clash Display Medium", 24 * -1)
)

canvas.create_rectangle(
    169.99937438964844,
    617.9944458007812,
    1808.0005950927734,
    622.9944458007812,
    fill="#231A49",
    outline="")

canvas.create_text(
    106.0,
    324.0,
    anchor="nw",
    text="CURRENTLY IN TREND",
    fill="#231A49",
    font=("Clash Display Semibold", 24 * -1)
)
window.resizable(False, False)
window.mainloop()
