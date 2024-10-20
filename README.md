Shi, Q. (2024). Automated Task Execution with CNN and NLP. GitHub. [https://github.com/username/repository](https://github.com/aqjshi/small_bot)]

# Automated Task Execution with CNN and NLP

## Project Overview

This project leverages **Convolutional Neural Networks (CNN)** and **Natural Language Processing (NLP)** to automate decision-making based on visual and text inputs. The purpose of this automation is to capture and analyze user interactions (mouse clicks, scrolls, and keyboard input) on a specified window area, process the visual data and text, and determine the most optimal course of action. Everything is stored locally and stored as a txt file. 


The core principle behind this project is simple: **If you are able to understand your task and separate it into steps that are repeatable, you do not have to do your job anymore**. By automating those steps, this system can take care of repetitive tasks through computer vision and text analysis, creating a dataset that serves as the foundation for decision-making models.  


The system uses:  

- **CNN** for visual similarity analysis (based on screenshots of user actions).
  
- **NLP** for text similarity (using OCR to extract and compare text from images).
  

## Project Files  


- **`generate_dataset.py`**: This script creates a dataset of actions by capturing screenshots and logging mouse/keyboard interactions. It doesn't require any arguments to run.
  
- **`bot.py`**: The core script that reads the created dataset, processes it, and uses a CNN combined with NLP-based text analysis to determine the best action. This also runs without requiring arguments.
  

## How It Works  


### Dataset Generation:  


- The `generate_dataset.py` script tracks user interactions with the mouse and keyboard.
  
- It takes screenshots of the specified window area each time a specific key (backtick \`) is pressed and logs the corresponding action (mouse click, keyboard press, or scroll) in a `log.txt` file.
  
- These actions are stored along with relative positions and button presses, and are later used for training or as input to determine the best action sequence.
  

### Automated Decision Making:  


- The `bot.py` script utilizes both **CNN for optical similarity** and **NLP for fine-grained text analysis**.
  
- Screenshots are processed through a CNN to find visual similarities with previously logged actions.
  
- Text in the images is extracted and compared using NLP techniques to further refine the matching process.
  
- The script determines the most relevant actions and automates their execution.
  

## How to Use

### 1. Clone the Repository  


```bash
git clone https://github.com/aqjshi/small_bot.git
cd small_bot
```


### Install Dependencies
Make sure you have Python installed. Install the required dependencies using:  

```bash
pip install -r requirements.txt
```
### Generate Dataset
To generate the dataset, run the following command. This will capture screenshots and log actions based on your mouse and keyboard inputs into a txt file called log.txt  


```bash
python generate_dataset.py
```
You'll be prompted to click on two points to calibrate the window where actions will be tracked.  

Each time you press the backtick (`) key, the script will take a screenshot and log the current actions.  


### Automate Actions Based on the Dataset
After generating the dataset, use the bot.py script to automate the process. The script reads the log.txt file and determines the best action to take based on visual and textual analysis: 


```bash
python bot.py
```
Find the most similar screenshots and log entries using a combination of CNN for optical analysis and NLP for text-based filtering.
Automatically execute the best matching actions.  


Automated Task Execution: The bot automates the process of determining the best actions based on both visual and textual analysis.  

Computer Vision Integration: A CNN is used to analyze screenshots, finding the most similar past actions and guiding the decision-making process.  

Text Analysis: NLP and OCR are employed to extract text from images and compare it to previously logged actions. 
 
Action Logging: Each user interaction is recorded, forming a comprehensive dataset for future decision-making.  






