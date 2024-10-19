import time
from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener
from pynput.mouse import Button
from pynput.keyboard import Key

# File paths
mouse_log_file = "log.txt"
key_log_file = "log.txt"
scroll_log_file = "log.txt"
'''
MP = Mouse Press
MR = Mouse Release
S = Scroll
KP = Key Press
KR = Key Release
SKP = Special Key Press
'''
# Function to log mouse click positions
def on_click(x, y, button, pressed):
    with open(mouse_log_file, "a") as f:
        if pressed:
            f.write(f"MP {x} {y} {button}\n")
        else:
            f.write(f"MR {x} {y} {button}\n")

# Function to log mouse scroll events
def on_scroll(x, y, dx, dy):
    with open(scroll_log_file, "a") as f:
        f.write(f"S {x} {y} {dx} {dy}\n")

# Function to log keyboard key press events
def on_press(key):
    with open(key_log_file, "a") as asf:
        try:
            f.write(f"KP {key.char}\n")
        except AttributeError:
            f.write(f"SKP {key}\n")

# Function to log keyboard key release events
def on_release(key):
    with open(key_log_file, "a") as f:
        f.write(f"KR: {key}\n")

# Set up the listeners
def start_listeners():
    # Mouse listener for clicks and scrolls
    mouse_listener = MouseListener(on_click=on_click, on_scroll=on_scroll)
    mouse_listener.start()

    # Keyboard listener for key presses
    keyboard_listener = KeyboardListener(on_press=on_press, on_release=on_release)
    keyboard_listener.start()

    # Keep the script running
    mouse_listener.join()
    keyboard_listener.join()

if __name__ == "__main__":
    print("Starting logging for mouse clicks, keyboard inputs, and scroll events...")
    start_listeners()
