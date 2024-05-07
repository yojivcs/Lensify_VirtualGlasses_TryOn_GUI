import tkinter as tk

class GlassesStoreGUI:
    def __init__(self, master):
        self.master = master
        master.title("Glasses Store")

        # Create menu
        menu = tk.Menu(master)
        master.config(menu=menu)

        home_menu = tk.Menu(menu)
        menu.add_cascade(label="HOME", menu=home_menu)
        home_menu.add_command(label="About")
        home_menu.add_command(label="Contact")

        glasses_menu = tk.Menu(menu)
        menu.add_cascade(label="GLASSES", menu=glasses_menu)
        glasses_menu.add_command(label="Shop Now")
        glasses_menu.add_command(label="Colour Code")
        glasses_menu.add_command(label="Lenses")
        glasses_menu.add_command(label="Chains")
        glasses_menu.add_command(label="Custom")

        # Create frames for glasses display
        display_frame = tk.Frame(master, bg="white")
        display_frame.pack(fill="both", expand=True)

        # Add some sample glasses images (replace with actual images)
        image1 = tk.Label(display_frame, text="Glasses 1")
        image1.pack(side="left", padx=10, pady=10)

        image2 = tk.Label(display_frame, text="Glasses 2")
        image2.pack(side="left", padx=10, pady=10)

        image3 = tk.Label(display_frame, text="Glasses 3")
        image3.pack(side="left", padx=10, pady=10)

root = tk.Tk()
my_gui = GlassesStoreGUI(root)
root.mainloop()