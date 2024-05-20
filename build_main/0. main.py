# Import the necessary modules
import subprocess
import sys
from pathlib import Path
from ctypes import windll

# Set DPI awareness
windll.shcore.SetProcessDpiAwareness(1)

# Define the path to the Homepage script
OUTPUT_PATH = Path(__file__).parent
homepage_script = OUTPUT_PATH / "1. Homepage.py"

# Run the Homepage script
subprocess.Popen([sys.executable, str(homepage_script)])
