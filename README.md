# Rock Paper Scissors Lizard Spock
The project I have created for the Arnold Clark Hackathon 2022 is an object detection program that recognises the gesture made by the user and displays an emoji at the top-left corner of their choice. To play against the computer the user can press 'p', the computer will randomly select a gesture which will be displayed on the top right corner alongside whether the user won or lost.

![ezgif com-gif-maker](https://user-images.githubusercontent.com/67346082/164284470-821606fd-ddf6-43e9-9b90-b2fe498d8b76.gif)

## How It's Made:

**Tech used:** Python, MediaPipe, and OpenCV

This project utilises the users' webcam to retrieve each frame. It then recognises if there are any hands present in the frame and overlays an exoskeleton of the bones and joints over the hand(s) in the frame. The location of each joint is then stored and transformed such that it is relative to the size of the frame. This is done to ensure distances and comparisons between different joints are bones remain accurate. Using this information, we check for the gesture being made by calculating the distance, (in some cases absolute and others relative) between different joints in the LEFT HAND. For example, for calculating if the gesture is scissors (the most troublesome) we obtain the distance between the tip of the index and the middle finger alongside the y-axis and if it's greater than 100px then it is classified as scissors and the scissor emoji will appear at the top left corner. 

To play a game with the PC the program waits for the letter 'p' to be clicked for 5ms. The game will only initiate if the player is showing a gesture, otherwise, the clicking is ignored. If the user is showing a gesture, then the program will make a random choice between rock, paper, scissors, lizard, and Spock and will compare the user and PC choice to determine if the player won. A message is then displayed on the top right corner alongside a record of wins in the bottom left corner. 

To stop running the camera and programme the user just needs to click 'q' for 5ms. 


## Future Optimizations:

Future optimizations that I look forward to making are: 
1) Implementing OOP to game.py as the code currently uses global variables and runs the main functionality outside of a function, which can certainly be improved.
2) Recognition of right-hand gestures, as I have hard-coded the distances using only the left hand (can you tell I am left-handed?). 
3) Add sound effects, I think it would be nice to add sound effects after a win/loss to enhance the experience. 
4) Add a timer on the screen after starting a game with the PC but before the answer is shown to mimic the "Rock, Paper, Scissors, Shoot".

I think these would be great additions to the game and would make it more interactive as well.

## Lessons Learned:

1) Try different solutions, don't get stuck. The solution presented is the result of numerous attempts to train a TensorFlow model locally (including hand labelling hundreds of photos) and using it to determine the gestures. However, I was unsuccessful and wasted valuable time doing it to eventually return to an arguably better, lightweight solution, which I am very satisfied with!  

2) On the technical side, I learned an immense amount as this is my first object detection project so learning how openCV and MediaPipe work and how to extract the position of joints to calculate distances and angles. Additionally, I learned how to create a requirements.txt file which I had not done before as well as learned how to use modules as part of my Python code. I have not implemented modules here mainly because of time constraints and the size of the script is not large enough to make significant gains in terms of separations of concerns. 

3) An upside of having failed attempts to implement the game I was able to learn how to train a TensorFlow Lite model in python and export it to use on handheld devices, which I may leverage in the future. However, the trade-off between training and validating a model and using pre-trained solutions is too large, so in future, I may just stay with MediaPipe.  
