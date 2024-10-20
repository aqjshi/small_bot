import time
from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener
from pynput.mouse import Button
from pynput.keyboard import Key
import re

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
// = comment ignore by the parser
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

def parse_log(log_file):
    actions = {}
    current_action = None

    # Define action patterns for matching
    action_patterns = ['MP', 'MR', 'S', 'KP', 'KR', 'SKP']
    
    with open(log_file, 'r') as f:
        for line in f:
            line = line.strip()

            # Ignore comments
            if line.startswith('//'):
                continue

            # Check for the start of a new action (action_0, action_1, etc.)
            action_match = re.match(r'action_(\d+)', line)
            if action_match:
                action_index = int(action_match.group(1))
                if action_index not in actions:
                    actions[action_index] = {
                        'commands': [],
                        'screenshot': None
                    }
                current_action = action_index

            # If we're inside an action, add commands from the line if they match the patterns
            if current_action is not None:
                if any(pattern in line for pattern in action_patterns):
                    actions[current_action]['commands'].append(line)

            # Check if the line is a screenshot and add it to the current action
            screenshot_match = re.match(r'// action_(\d+) Screenshot saved as (.+)', line)
            if screenshot_match:
                action_index = int(screenshot_match.group(1))
                screenshot_file = screenshot_match.group(2).strip()
                if action_index in actions:
                    actions[action_index]['screenshot'] = screenshot_file

    return actions

if __name__ == "__main__":
    print("Starting logging for mouse clicks, keyboard inputs, and scroll events...")
    # start_listeners()
    actions = parse_log("log.txt")
    #print entire set of actions 
    print(actions)