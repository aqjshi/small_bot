import pyautogui
import time
import math
import cv2
import os
import numpy as np

# Capture a fixed 400x400 screenshot around the cursor position
def take_screenshot_around_cursor():
    current_x, current_y = pyautogui.position()
    min_x = max(current_x - 75, 0)
    min_y = max(current_y - 75, 0)
    max_x = min(current_x + 75, pyautogui.size()[0])
    max_y = min(current_y + 75, pyautogui.size()[1])

    screenshot = pyautogui.screenshot(region=(min_x, min_y, max_x - min_x, max_y - min_y))
    screenshot = np.array(screenshot)  # Convert to numpy array for OpenCV
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)  # Convert to grayscale
    return screenshot, min_x, min_y

# Apply Canny edge detection
def apply_edge_detection(image):
    edges = cv2.Canny(image, 50, 100)  # Adjusted thresholds for performance
    return edges

# Optimized function to find the first button in the screenshot using BFS approach
def find_first_button_bfs(screenshot, button_template_folder):
    search_region_edges = apply_edge_detection(screenshot)  # Apply edge detection to the search region

    for template_file in os.listdir(button_template_folder):
        template_path = os.path.join(button_template_folder, template_file)
        template = cv2.imread(template_path, 0)  # Load template in grayscale

        if template is None:
            continue

        # Perform edge detection on the template
        template_edges = apply_edge_detection(template)

        # Perform template matching
        result = cv2.matchTemplate(search_region_edges, template_edges, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        # If a match is found, return its location
        if max_val > 0.8:  # Use a threshold to find a good match
            h, w = template_edges.shape
            button_center = (max_loc[0] + w // 2, max_loc[1] + h // 2)
            return button_center

    return None

# Function to move to the first button detected
def move_to_first_button(button_template_folder):
    # Capture screenshot around the mouse cursor
    screenshot, min_x, min_y = take_screenshot_around_cursor()

    # Find the first button using BFS
    button_center = find_first_button_bfs(screenshot, button_template_folder)

    if button_center is not None:
        # Adjust the coordinates based on the screenshot region
        adjusted_x = min_x + button_center[0]
        adjusted_y = min_y + button_center[1]
        print(f"Button detected at: {adjusted_x}, {adjusted_y}. Moving to it.")

        # Move to the center of the button
        pyautogui.moveTo(adjusted_x, adjusted_y, duration=0.2)
        print("Task completed. Exiting.")
    else:
        print("No button found. Exiting.")

if __name__ == '__main__':
    button_template_folder = 'data/buttons'  
    for i in range(10):
        move_to_first_button(button_template_folder)
        time.sleep(.2) 
