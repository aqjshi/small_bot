import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# Initialize the Chrome driver
def init_driver(chrome_service_path='/opt/homebrew/bin/chromedriver'):
    chrome_service = Service(chrome_service_path)
    return webdriver.Chrome(service=chrome_service)

# Function to open the Google Snake game
def open_snake_game(driver):
    driver.get("https://www.google.com/search?q=snake")
    time.sleep(2)  # Let the page load

# Function to simulate mouse click at given X and Y coordinates
def click_at_position(driver, x, y):
    try:
        driver.execute_script(f"""
            var element = document.elementFromPoint({x}, {y});
            if (element) {{
                var event = new MouseEvent('click', {{
                    'view': window,
                    'bubbles': true,
                    'cancelable': true,
                    'clientX': {x},
                    'clientY': {y}
                }});
                element.dispatchEvent(event);
            }} else {{
                console.log('No element found at the given coordinates');
            }}
        """)
        print(f"Mouse click simulated at X: {x}, Y: {y}")
        return True
    except Exception as e:
        print(f"Error simulating mouse click at X: {x}, Y: {y}: {e}")
        return False

# Function to dynamically find the "Play" button by aria-label and adjust its constraints
def find_and_click_play_button(driver):
    try:
        # Locate the 'Play' button by its aria-label
        play_button = driver.find_element(By.CSS_SELECTOR, '[aria-label="Play"]')
        location = play_button.location
        size = play_button.size

        # Dynamically set constraints based on the button's position and size
        x_min = location['x']
        y_min = location['y']
        x_max = x_min + size['width']
        y_max = y_min + size['height']

        print(f"Dynamic Play button found at X={x_min}, Y={y_min}, Width={size['width']}, Height={size['height']}")

        # Click the Play button within the dynamically calculated constraints
        click_at_position(driver, x_min + 10, y_min + 10)
        return True
    except Exception as e:
        print(f"Error finding or clicking the 'Play' button: {e}")
        return False

def play_game(game_area):
    while True:
        game_area.send_keys(Keys.ARROW_RIGHT)
        time.sleep(.5)
        game_area.send_keys(Keys.ARROW_DOWN)
        time.sleep(.5)
        game_area.send_keys(Keys.ARROW_LEFT)
        time.sleep(.5)
        game_area.send_keys(Keys.ARROW_UP)
        time.sleep(.5)

# Main function to run the full workflow
def main():
    driver = init_driver()
    
    try:
        # Open the game
        open_snake_game(driver)

        # Click the initial play button (coordinates may need to be adapted)
        if click_at_position(driver, 261, 492):
            print("Initial 'Play' button clicked. Waiting for dialog 'Play' button...")
            time.sleep(2)

            # Dynamically find and click the dialog "Play" button
            if find_and_click_play_button(driver):
                print("Dialog 'Play' button clicked. Starting the game...")

                # Locate the game area (usually the body or canvas element)
                game_area = driver.find_element(By.TAG_NAME, 'body')
                game_area.click()

                # Start playing the game (this can be extended with actual gameplay logic)
                play_game(game_area)
            else:
                print("Failed to find or click dialog 'Play' button.")
        else:
            print("Initial 'Play' button not clicked. Cannot proceed.")

    finally:
        # Close the browser after interaction
        driver.quit()

if __name__ == "__main__":
    main()
