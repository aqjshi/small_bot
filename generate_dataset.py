import pyautogui
import os
from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener, Key
from pynput.mouse import Button
import time

# Initialize the screenshot counter
i = 110
log_file_path = "log.txt"



# Calibrate window to capture the web area, click to activate record xy
def calibrate_window():
    calibration_points = []
    
    def on_click(x, y, button, pressed):
        # Only capture left button clicks
        if pressed and button == Button.left:
            calibration_points.append((x, y))
            print(f"Captured point: {x}, {y}")
            # Stop listener after capturing two points
            if len(calibration_points) >= 2:
                return False  # Stop the listener

    print("Please click the top-left corner of the web area...")
    
    # Start listener and ensure it is properly closed
    try:
        with MouseListener(on_click=on_click) as listener:
            listener.join()  # Wait until two clicks are captured
    finally:
        if listener.running:
            listener.stop()  # Ensure the listener is stopped

    # After two clicks are captured, assign to variables
    (x_0, y_0), (x_1, y_1) = calibration_points
    # cast to int
    x_0, y_0, x_1, y_1 = map(int, [x_0, y_0, x_1, y_1])

    print(f"Top-left corner: {x_0}, {y_0}")
    print(f"Bottom-right corner: {x_1}, {y_1}")

    return x_0, y_0, x_1, y_1

web_x_0, web_y_0, web_x_1, web_y_1 = calibrate_window()

# Function to take screenshot of defined window area and save with the incremented filename
def take_screenshot(min_x, min_y, max_x, max_y, action_number):
    screenshot = pyautogui.screenshot(region=(min_x, min_y, max_x - min_x, max_y - min_y))
    screenshot_path = f"data/images/action_{action_number}.png"
    screenshot.save(screenshot_path)
    return screenshot_path

# Function to log mouse click positions and take screenshot after each click, with action number
def on_click(x, y, button, pressed):
    global i
    relative_x = x - web_x_0
    relative_y = y - web_y_0
    with open("log.txt", "a") as f:
        if pressed:
            f.write(f"action_{i} MP {relative_x} {relative_y} {button}\n")
        else:
            f.write(f"action_{i} MR {relative_x} {relative_y} {button}\n")
        f.flush()  # Force write to file immediately
    return x, y

def on_scroll(x, y, dx, dy):
    relative_x = x - web_x_0
    relative_y = y - web_y_0
    with open("log.txt", "a") as f:
        f.write(f"action_{i} S {relative_x} {relative_y} {dx} {dy}\n")
        f.flush()  # Force write to file immediately

# Function to log keyboard key press events and increment action number on backtick (`) press
def on_press(key):
    global i
    with open("log.txt", "a") as f:
        try:
            f.write(f"action_{i} KP {key.char}\n")
            if key.char == "`":  # Check if the backtick key was pressed
                i += 1  # Increment screenshot label index
                f.write(f"// Backtick pressed, incrementing action number to {i}\n")
                screenshot_path = take_screenshot(web_x_0, web_y_0, web_x_1, web_y_1, i)
            f.flush()  # Force write to file immediately
        except AttributeError:
            f.write(f"action_{i}: SKP {key}\n")
            f.flush()  # Force write to file immediately

# Function to log keyboard key release events
def on_release(key):
    global i
    with open("log.txt", "a") as f:
        f.write(f"action_{i} KR {key}\n")
        f.flush()  # Force write to file immediately

# Set up the listeners for mouse and keyboard events
def start_listeners():
    mouse_listener = MouseListener(on_click=on_click, on_scroll=on_scroll)
    keyboard_listener = KeyboardListener(on_press=on_press, on_release=on_release)

    mouse_listener.start()
    keyboard_listener.start()

    mouse_listener.join()
    keyboard_listener.join()


# Start the listeners
start_listeners()
