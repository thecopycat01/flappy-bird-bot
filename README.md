# flappy-bird-bot


The flappy bird game is actually an android game from an unknown developer

here are the things used by me:-

1)Bluestacks to play android game in laptop
2)roboflow to create dataset which I used to train yolov8 model using screenshots of playing the game
3)pyautogui:- to take screenshot and to click in screen . I am taking only screenshot of the region of the laptop which contains the game screen of bluestacks


Characteristics of flappy bird game:------------------------------------------------------------

We can tap the screen anywhere to make flappy bird jump.
The flappy bird need to avoid roof,ground,pillars and pass through the gap between two pillars, one pillar attached to roof and one to ground.
As the game progresses it doesn't affect the speed of the game.

I want to make the bot play game to avoid crashing and also identify pillars behind bird and ahead of it.
if bird is in the gap the bird should jump after 0.5 seconds to avoid crashing on top or bottom pillar while jumping 
