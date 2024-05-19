import tkinter as tk
from homepage import HomePage
from about_us import AboutUsPage

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Lensify")
        self.geometry("1920x980")
        self.configure(bg="#FFFFFF")

        # Container for all frames
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (HomePage, AboutUsPage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
