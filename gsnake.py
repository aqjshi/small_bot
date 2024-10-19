import pyautogui
import pytesseract
from PIL import Image
import cv2
import numpy as np
import time
import os

# Path to Tesseract executable (modify this path based on your setup)
pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'

# Take a screenshot
def take_screenshot():
    screenshot = pyautogui.screenshot()
    screenshot.save("screenshot.png")
    #save to file
    return screenshot

def preprocess_image(screenshot_path):
    image = cv2.imread(screenshot_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)  # Increase contrast
    return Image.fromarray(binary)


# Function to use OCR to find keyword
def find_keyword_in_screenshot(keyword, screenshot_path):
    image = preprocess_image(screenshot_path)  # Preprocess the image
    # data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
    
    # Use custom Tesseract config to improve detection accuracy
    custom_config = r'--oem 3 --psm 6'  # Adjust this based on your needs
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT, config=custom_config)


    # debug
    # print("Detected words:", data['text'])

    # Loop over each word found by pytesseract
    for i, word in enumerate(data['text']):
        if word.lower() == keyword.lower():
            # Get the bounding box coordinates of the word
            x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
            os.remove(screenshot_path)
            return (x, y, w, h)
    
    return None


# Function to click on the found keyword
def click_on_word(x, y, w, h):
    # Calculate the center of the word
    click_x = x + w / 2 
    click_y = y + h / 2
    
    # Move the mouse to the word's position and click
    pyautogui.moveTo(click_x, click_y)
    
    # double click
    pyautogui.doubleClick()


def open_file(keyword="KEYWORD"):
    screenshot0 = take_screenshot()
    x, y, w, h = find_keyword_in_screenshot(keyword, "screenshot.png")

    # Calculate the center of the word
    click_x = x + w / 2 
    click_y = y + h / 2
    print(f"Found at position (X: {x}, Y: {y}) with size (W: {w}, H: {h})")
    # Move the mouse to the word's position and click
    pyautogui.moveTo(click_x, click_y)


    #OPENING FILES IN MAC
    pyautogui.click(button='right')
    time.sleep(1)
    screenshot = take_screenshot()
    screenshot.save("screenshot.png")

    keyword = "Open"
    result = find_keyword_in_screenshot(keyword, "screenshot.png")
    if result:
        x, y, w, h = result
        print(f"Found at position (X: {x}, Y: {y}) with size (W: {w}, H: {h})")
        
        # Step 3: Click on the keyword
        click_on_word(x, y, w, h)
    else:
        print(f"Not found on the screen.")
    
    



def play_snake(keyword="PLAY"):
    # Step 1: Take a screenshot
    screenshot0 = take_screenshot()
    x, y, w, h = find_keyword_in_screenshot(keyword, "screenshot.png")
    click_on_word(x, y, w, h)
    time.sleep(1)


    screenshot2 = take_screenshot()
    x, y, w, h = find_keyword_in_screenshot(keyword, "screenshot.png")
    click_on_word(x, y, w, h)
    time.sleep(1)

    pyautogui.press('right')
    time.sleep(0.5)
    pyautogui.press('down')
    time.sleep(0.5)
    pyautogui.press('left')
    time.sleep(0.5)
    pyautogui.press('up')
    time.sleep(0.5)


# Main function
def main():
    play_snake(keyword="PLAY")
    time.sleep(3)
    open_file(keyword="KEYWORD")

if __name__ == "__main__":
    main()
