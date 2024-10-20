import os
import re
import pyautogui
from pynput.mouse import Listener as MouseListener
from pynput.mouse import Button
from PIL import Image, ImageChops, ImageStat
import pyautogui
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from torchvision import models
from PIL import Image
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import time
import nltk
from nltk.tokenize import word_tokenize
import pytesseract
from difflib import SequenceMatcher
from tracer import  move_to_first_button
nltk.download('punkt')

# Define a class to store actions
class Action:
    def __init__(self, index):
        self.index = index
        self.screenshot = None
        self.commands = []

    def add_command(self, command):
        self.commands.append(command)

    def set_screenshot(self, screenshot):
        self.screenshot = screenshot

# Function to parse the log file
def parse_log(log_file):
    actions = {}
    current_action = None

    with open(log_file, 'r') as f:
        for line in f:
            line = line.strip()
            
            # Tokenize the line
            tokens = word_tokenize(line)

            # Match action pattern using regular expressions
            action_match = re.match(r'action_(\d+)', line)
            if action_match:
                action_index = int(action_match.group(1))
                current_action = Action(action_index)
                actions[action_index] = current_action
                continue
            
            # Screenshot parsing
            screenshot_match = re.match(r'// action_(\d+) Screenshot saved as (.+)', line)
            if screenshot_match:
                action_index = int(screenshot_match.group(1))
                screenshot_file = screenshot_match.group(2).strip()
                if action_index in actions:
                    actions[action_index].set_screenshot(screenshot_file)
                continue

            # Capture remaining commands for the current action
            if current_action is not None and line:
                current_action.add_command(line)

    return actions


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

# Define a class to store actions
class Action:
    def __init__(self, index):
        self.index = index
        self.screenshot = None
        self.commands = []

    def add_command(self, command):
        self.commands.append(command)

    def set_screenshot(self, screenshot):
        self.screenshot = screenshot

# Function to parse the log file
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
                    actions[action_index] = Action(action_index)
                current_action = actions[action_index]

            # If we're inside an action, add commands from the line if they match the patterns
            if current_action is not None:
                if any(pattern in line for pattern in action_patterns):
                    current_action.add_command(line)

            # Check if the line is a screenshot and add it to the current action
            screenshot_match = re.match(r'// action_(\d+) Screenshot saved as (.+)', line)
            if screenshot_match:
                action_index = int(screenshot_match.group(1))
                screenshot_file = screenshot_match.group(2).strip()
                if action_index in actions:
                    actions[action_index].set_screenshot(screenshot_file)

    return actions


# Function to take a screenshot of the current window area
def take_screenshot(min_x, min_y, max_x, max_y):
    screenshot = pyautogui.screenshot(region=(min_x, min_y, max_x - min_x, max_y - min_y))
    screenshot_path = f"data/current_images/current_screenshot.png"
    screenshot.save(screenshot_path)
    return screenshot_path

# Load pre-trained CNN model (VGG16) for feature extraction
def get_cnn_model():
    model = models.resnet50(pretrained=True)
    model = nn.Sequential(*list(model.children())[:-1])
    model.eval()
    return model




# Function to extract features using CNN
def extract_features(image_path, model, transform):
    image = Image.open(image_path).convert('RGB')
    image = transform(image).unsqueeze(0)  # Add batch dimension
    with torch.no_grad():
        features = model(image)
    return features.numpy()

# Function to find the most similar image using CNN and cosine similarity
# def find_most_similar_image(current_screenshot_path, image_dir, model, transform):
#     current_features = extract_features(current_screenshot_path, model, transform)
#     most_similar_image = None
#     highest_similarity = -1

#     for image_file in os.listdir(image_dir):
#         image_path = os.path.join(image_dir, image_file)
#         stored_features = extract_features(image_path, model, transform)
#         similarity = cosine_similarity(current_features, stored_features)[0][0]

#         if similarity > highest_similarity:
#             highest_similarity = similarity
#             most_similar_image = image_path

#     return most_similar_image, highest_similarity

from skimage.metrics import structural_similarity as ssim
import cv2

# Function to compute SSIM between two images
def compute_ssim(image1_path, image2_path):
    img1 = cv2.imread(image1_path, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(image2_path, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.resize(img2, img1.shape[::-1])  # Ensure same size
    similarity, _ = ssim(img1, img2, full=True)
    return similarity

# Modify this function to use SSIM instead of cosine similarity
def find_most_similar_image_ssim(current_screenshot_path, image_dir):
    most_similar_image = None
    highest_similarity = -1

    for image_file in os.listdir(image_dir):
        image_path = os.path.join(image_dir, image_file)
        similarity = compute_ssim(current_screenshot_path, image_path)
        
        if similarity > highest_similarity:
            highest_similarity = similarity
            most_similar_image = image_path

    return most_similar_image, highest_similarity

def extract_text_from_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text.strip()

# Function to compare two text strings for similarity using SequenceMatcher
def text_similarity(text1, text2):
    return SequenceMatcher(None, text1, text2).ratio()

# Modify this function to find the most similar image based on text extracted by OCR
def find_most_similar_image_by_text(current_screenshot_path, image_dir):
    current_text = extract_text_from_image(current_screenshot_path)
    most_similar_image = None
    highest_similarity = -1

    for image_file in os.listdir(image_dir):
        image_path = os.path.join(image_dir, image_file)
        stored_text = extract_text_from_image(image_path)
        similarity = text_similarity(current_text, stored_text)

        if similarity > highest_similarity:
            highest_similarity = similarity
            most_similar_image = image_path

    return most_similar_image, highest_similarity


# Function to execute the actions and adjust x, y with web_x_0 and web_y_0 offsets
def move_mouse_stepwise(current_x, current_y, target_x, target_y, steps):
    """
    Moves the mouse stepwise from the current position to the target position.
    
    :param current_x: Current x position of the mouse
    :param current_y: Current y position of the mouse
    :param target_x: Target x position of the mouse
    :param target_y: Target y position of the mouse
    :param steps: Number of steps to break the movement into
    """
    # Calculate the distance to move in each step
    step_x = (target_x - current_x) / steps
    step_y = (target_y - current_y) / steps

    for i in range(steps):
        # Move the mouse incrementally
        current_x += step_x
        current_y += step_y
        pyautogui.moveTo(current_x, current_y)
        time.sleep(0.01)  # Small delay to simulate smooth movement

def execute_action(command, min_x, min_y, button_template_path, steps=5):
    """
    Executes the action based on the parsed command and moves the mouse in steps,
    adjusting to the closest button if necessary.
    
    :param command: The command string to be executed
    :param min_x: Minimum x offset to adjust the target position
    :param min_y: Minimum y offset to adjust the target position
    :param button_template_path: Path to the button template image for template matching
    :param steps: Number of steps for stepwise mouse movement
    """
    parts = command.split()

    # Example for Mouse Press (MP) action
    if parts[1] == 'MP':  
        print("mouse pressing")
        target_x = float(parts[2]) + min_x
        target_y = float(parts[3]) + min_y

        # Adjust target to the closest button-like element

        # Get the current position of the mouse
        current_x, current_y = pyautogui.position()

        # Debug the coordinates
        print(f"Moving from ({current_x}, {current_y}) to ({target_x}, {target_y})")

        # Move the mouse stepwise before performing any clicks
        move_mouse_stepwise(current_x, current_y, target_x, target_y, steps)
        move_to_first_button('data/')

        # Perform the click after moving
        pyautogui.mouseDown(button='left')
        time.sleep(0.05)
        pyautogui.mouseUp(button='left')
        print(f"Mouse pressed at ({target_x}, {target_y})")


    # Mouse Release (MR) action
    elif parts[1] == 'MR':  
        target_x = float(parts[2]) + min_x
        target_y = float(parts[3]) + min_y
        # Get the current position of the mouse
        current_x, current_y = pyautogui.position()

        # Move the mouse stepwise to the position
        move_mouse_stepwise(current_x, current_y, target_x, target_y, steps)

        # Perform the mouse release
        button = parts[3].lower().replace('button.', '')
        pyautogui.mouseUp(button='left')
        print(f"Mouse released at ({target_x}, {target_y}) with {button} button")

    # Mouse Scroll (S) action
    elif parts[1] == 'S':  
        target_x = float(parts[2]) + min_x
        target_y = float(parts[3]) + min_y

        # Get current position of the mouse
        current_x, current_y = pyautogui.position()

        # Move the mouse stepwise to the scroll position
        move_mouse_stepwise(current_x, current_y, target_x, target_y, steps)

        # Perform the scroll action
        scroll_amount = int(parts[5])
        pyautogui.scroll(scroll_amount)
        print(f"Scrolled at ({target_x}, {target_y}) by {scroll_amount}")
    
    # Key Press (KP) action
    elif parts[1] == 'KP':  
        key = parts[2]
        pyautogui.keyDown(key)
        print(f"Key pressed: {key}")

    # Key Release (KR) action
    elif parts[1] == 'KR':  
        key = parts[2]
        pyautogui.keyUp(key)
        print(f"Key released: {key}")


# Main function
if __name__ == '__main__':
    log_file = 'log.txt'  # Your log file
    actions = parse_log(log_file)
    
    # Calibrate window
    web_x_0, web_y_0, web_x_1, web_y_1 = calibrate_window()

    for i in range(10):
        time.sleep(5)  # Wait for 1 second before the next iteration
        # Take a screenshot
        current_screenshot = take_screenshot(web_x_0, web_y_0, web_x_1, web_y_1)

        # Load CNN model
        cnn_model = get_cnn_model()
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])

        # Step 1: Find most similar image optically using SSIM
        image_directory = 'data/images'
        most_similar_image, similarity = find_most_similar_image_ssim(current_screenshot, image_directory)

        # Step 2: Fine-grain filter using text comparison (OCR)
        most_similar_image_by_text, similarity_score = find_most_similar_image_by_text(current_screenshot, image_directory)

        # Get actions associated with the most similar image
        similar_actions = actions[int(re.search(r'\d+', most_similar_image_by_text).group())].commands

        # Execute actions
        for action in similar_actions:
            execute_action(action, web_x_0, web_y_0, 'data/button_template.png')
