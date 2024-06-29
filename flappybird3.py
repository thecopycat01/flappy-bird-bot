import threading
import pyautogui
import keyboard
from PIL import Image
from ultralytics import YOLO
import random
import time
from operator import itemgetter

xrand=random.randint(1516,1845)
yrand=random.randint(245,623)

# Function to play the game
def play_game(decision):
        time.sleep(0.5)
        pyautogui.moveTo((xrand,yrand))
        pyautogui.click((xrand,yrand))
        print('clicking')
        

# Function to take screenshots
def take_screenshot(stop_event, model):
    screenx_center = 3840/2
    screeny_center = 2160/2
    pyautogui.FAILSAFE = False

    while not stop_event.is_set():
        decision = {
            "bird": False,
            "pillars": False,
            "roof": False,
            "ground": False,
            "name": False,
            "replay": False,
            "start": False,
            "pillars_coords":[],
            "roof_coords":[],
            "ground_coords":[],
            "left_pillars":[],
            "right_pillars":[],
            "middlex_pillars":[],
            "top_pillars":[],
            "bottom_pillars":[],
            "middley_pillars":[],
            

        }

        # Take screenshot
        screenshot = pyautogui.screenshot()
        screenshot = Image.frombytes('RGB', screenshot.size, screenshot.tobytes())
        
        results = model([screenshot], conf=.65)  # return a list of Results objects
        boxes = results[0].boxes.xyxy.tolist()
        classes = results[0].boxes.cls.tolist()
        names = results[0].names
        confidences = results[0].boxes.conf.tolist()

        # Process results list
        for box, cls, conf in zip(boxes, classes, confidences):
            x1, y1, x2, y2 = box
            
            center_x=225
            center_y=380

            name = names[int(cls)]
            
            if name=="bird":
                decision["bird"] = True
                decision["bird_coords"]=[x1,y1,x2,y2]
            elif name=="name":
                decision["name"] = True
                decision["name_coords"]=[x1,y1,x2,y2]
            elif name=="start":
                decision["start"] = True
                decision["start_coords"]=[x1,y1,x2,y2]
            elif name=="replay":
                decision["replay"] = True
                decision["replay_coords"]=[x1,y1,x2,y2]
            # To get most relevant roof coordinates.
            elif name=="roof":
                decision["roof"] = True
                if len(decision["roof_coords"])!=0:
                    for i in range(len(decision["roof_coords"])):
                        if y2>decision["roof_coords"][i][3]:
                            del decision["roof_coords"][i]
                            decision["roof_coords"].append([x1,y1,x2,y2])
                else:
                    decision["roof_coords"].append([x1,y1,x2,y2])
            # To get most relevant ground coordinates.
            elif name=="ground":
                decision["ground"] = True
                if len(decision["ground_coords"])!=0:
                    for i in range(len(decision["ground_coords"])):
                        if y1<decision["ground_coords"][i][1]:
                            del decision["ground_coords"][i]
                            decision["ground_coords"].append([x1,y1,x2,y2])
                else:
                    decision["ground_coords"].append([x1,y1,x2,y2])
            # To gat pillar coordinates
            elif name=="pillar":
                decision["pillar"] = True
                if x2<center_x-80:
                    decision["left_pillars"].append([x1,y1,x2,y2])
                elif x2>=center_x-80 and x2<center_x+45:
                    decision["middlex_pillars"].append([x1,y1,x2,y2])
                elif x1>center_x+45:
                    decision["right_pillars"].append([x1,y1,x2,y2])
                elif x1<=center_x+45:
                    decision["middlex_pillars"].append([x1,y1,x2,y2])
                if y2<center_y-80:
                    decision["top_pillars"].append([x1,y1,x2,y2])
                elif y2>=center_y-80 and y2<center_y+45:
                    decision["middley_pillars"].append([x1,y1,x2,y2])
                elif y1>center_y+45:
                    decision["bottom_pillars"].append([x1,y1,x2,y2])
                elif y1<=center_y+45:
                    decision["middley_pillars"].append([x1,y1,x2,y2])
                

            
        play_game(decision)
        time.sleep(0.1)   # Add a delay to avoid over-clicking

# Main function
def main():
    print(pyautogui.KEYBOARD_KEYS)
    model = YOLO('best.pt')
    stop_event = threading.Event()
    
    # Create and start the screenshot thread
    screenshot_thread = threading.Thread(target=take_screenshot, args=(stop_event, model))
    screenshot_thread.start()

    # Listen for keyboard input to quit the program
    keyboard.wait("q")

    # Set the stop event to end the screenshot thread
    stop_event.set()

    # Wait for the screenshot thread to finish
    screenshot_thread.join()

    print("Program ended.")

if __name__ == "__main__":
    main()
