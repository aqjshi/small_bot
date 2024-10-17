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
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
    
    # Loop over each word found by pytesseract
    for i, word in enumerate(data['text']):
        if word.lower() == keyword.lower():
            # Get the bounding box coordinates of the word
            x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
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

    #OPENING FILES IN MAC
#     pyautogui.click(button='right')
#     time.sleep(.5)
#     # Mouse clicked at X: 1991.65625, Y: 1085.2265625
#     # Mouse clicked at X: 2026.2890625, Y: 925.625
# # 34.6328125, -159.6015625
#     pyautogui.moveTo(click_x + 35, click_y - 165)
#     #left click
#     pyautogui.click()
#     time.sleep(.5)

# Main function
def main():
    keyword = "PLAY"  # Change to the word you are looking for

    # Step 1: Take a screenshot
    screenshot = take_screenshot()

    # Step 2: Find the keyword in the screenshot
    result = find_keyword_in_screenshot(keyword, "screenshot.png")
    
    #delete the screenshot
    os.remove("screenshot.png")
    if result:
        x, y, w, h = result
        print(f"Found at position (X: {x}, Y: {y}) with size (W: {w}, H: {h})")
        
        # Step 3: Click on the keyword
        click_on_word(x, y, w, h)
    else:
        print(f"Not found on the screen.")

    time.sleep(1)
    screenshot2 = take_screenshot()
    screenshot2.save("screenshot2.png")  # Save with a different name
    result2 = find_keyword_in_screenshot(keyword, "screenshot2.png")


    # Step 2: Find the keyword in the screenshot
    result2 = find_keyword_in_screenshot(keyword, "screenshot2.png")
    
    while( not result2):
        result2 = find_keyword_in_screenshot(keyword, "screenshot2.png")

    if result2:
        x, y, w, h = result2
        print(f"Found at position (X: {x}, Y: {y}) with size (W: {w}, H: {h})")
        
        # Step 3: Click on the keyword
        click_on_word(x, y, w, h)

    else:
        print(f"Not found on the screen.")

    pyautogui.press('right')
    time.sleep(0.5)
    pyautogui.press('down')
    time.sleep(0.5)
    pyautogui.press('left')
    time.sleep(0.5)
    pyautogui.press('up')
    time.sleep(0.5)

if __name__ == "__main__":
    main()
