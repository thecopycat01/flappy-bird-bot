import threading
import pyautogui
import keyboard
from PIL import Image
from ultralytics import YOLO
import random
import time
from operator import itemgetter
import queue

xrand=random.randint(1516,1845)
yrand=random.randint(245,623)
#decisive functions
def maintain(xrand,yrand):
    print('maintain')
    pyautogui.moveTo(xrand,yrand)
    pyautogui.click(xrand,yrand)
    time.sleep(0.2)


def maintaincenter(decision,xrand,yrand):
    print('maintaincenter')
    print('bird:',decision['bird'])
    print('ground:',decision['ground'])
    print('roof:',decision['roof'])
    if decision["bird"]==True and decision["ground"]==True and decision["roof"]==True:
        if decision["bird_coords"][0][3] > (decision["ground_coords"][0][1]-decision["roof_coords"][0][3])/2:
            pass
        elif decision["bird_coords"][0][3] == (decision["ground_coords"][0][1]-decision["roof_coords"][0][3])/2:
            time.sleep(0.4)
            pyautogui.click(xrand,yrand)
        elif decision["bird_coords"][0][3] < (decision["ground_coords"][0][1]-decision["roof_coords"][0][3])/2:
            pyautogui.moveTo(xrand,yrand)
            pyautogui.click(xrand,yrand)
    else:
        maintain()
def compare(decision,xrand,yrand):
    print('compare')
    if len(decision["pillar_coords"])==1:
        if decision["bird_coords"][0][1] in range(int(decision["pillar_coords"][0][3])):
            pass
        elif decision["bird_coords"][0][1] not in range(int(decision["pillar_coords"][0][3]+10)):
            maintain(xrand,yrand)

    elif len(decision["pillar_coords"])==2:
        if decision["bird_coords"][0][1] in range(int(decision["pillar_coords"][0][3])) :
            pass
        elif decision["bird_coords"][0][1] in range(int(decision["pillar_coords"][1][1]), int(decision["pillar_coords"][1][3])):
            pyautogui.moveTo(xrand,yrand)
            pyautogui.click(xrand,yrand)
        elif decision["bird_coords"][0][1] in range(int(decision["pillar_coords"][1][1]+10), int(decision["pillar_coords"][1][3])):
            pyautogui.moveTo(xrand,yrand)
            pyautogui.doubleClick(xrand,yrand)
        elif decision["bird_coords"][0][1] not in range(int(decision["pillar_coords"][0][3]+10)) and decision["bird_coords"][0][1] not in range(int(decision["pillar_coords"][1][1]), int(decision["pillar_coords"][1][3])):
            maintain(xrand,yrand)
        


#Function to play the game
def play_game(decision):
        
        if decision["bird"]==True and decision["pillar"]==False:
            maintaincenter(decision,xrand,yrand)
        elif decision["bird"]==True and decision["pillar"]==True:
            compare(decision,xrand,yrand)
        else:
            pass
        
        
            

# Function to take screenshots
def take_screenshot(stop_event, model):
    screenx_center = 3840/2
    screeny_center = 2160/2
    pyautogui.FAILSAFE = False

    while not stop_event.is_set():
        decision = {
            "bird": False,
            "pillar": False,
            "roof": False,
            "ground": False,
            "name": False,
            "replay": False,
            "start": False,

            "bird_coords":[],
            "pillar_coords":[],
            "roof_coords":[],
            "ground_coords":[],
            "name_coords":[],
            "replay_coords":[],
            "start_coords":[],
            "new_pillar_coords":[]
            

        }

        # Take screenshot
        screenshot = pyautogui.screenshot()
        screenshot = Image.frombytes('RGB', screenshot.size, screenshot.tobytes())
        
        results = model([screenshot], conf=.3)  # return a list of Results objects
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
                decision["bird_coords"].append([x1,y1,x2,y2])
            elif name=="name":
                decision["name"] = True
                decision["name_coords"].append([x1,y1,x2,y2])
            elif name=="start":
                decision["start"] = True
                decision["start_coords"].append([x1,y1,x2,y2])
            elif name=="replay":
                decision["replay"] = True
                decision["replay_coords"].append([x1,y1,x2,y2])
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
            # To get pillar coordinates
            elif name=="pillar":
                decision["pillar"] = True
                decision["pillar_coords"].append([x1,y1,x2,y2])
                
            else:
                pass
        if len(decision["pillar_coords"])!=0:
                    if decision["bird"]==True and decision["bird_coords"][0][2]<=x2:
                        decision["new_pillar_coords"].append([x1,y1,x2,y2])
        else:
            pass


        if decision["bird"]==True and decision["pillar"]==True:
            if len(decision["new_pillar_coords"])>1:
                decision["newpillar"]=sorted(decision["pillar"],key=itemgetter(1))
        else:
            pass
        
        play_game(decision)
        

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
