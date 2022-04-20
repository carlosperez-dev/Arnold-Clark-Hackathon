import mediapipe as mp
import cv2
import numpy as np
#import uuid
import os
from datetime import datetime
import random

def setImagesPaths(folderPath):
    myList = os.listdir(folderPath)
    overLayList = []
    for imPath in myList:
        if imPath!= '.DS_Store':
            image = cv2.imread(f'{folderPath}/{imPath}')
            #print(f'{folderPath}/{imPath}')
            overLayList.append(image)
    return overLayList

def overlayExoSkeleton(frame):
    # BGR 2 RGB
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)    
    # Flip on horizontal
    image = cv2.flip(image, 1)
    # Set flag
    image.flags.writeable = False    
    # Detections
    results = hands.process(image)    
    # Set flag to true
    image.flags.writeable = True   
    # RGB 2 BGR
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)   
    return results, image     

def renderExoSkeleton(results, image):
    lmList = []
    if results.multi_hand_landmarks:
        for num, hand in enumerate(results.multi_hand_landmarks):
            mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS, 
                                    mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                                    mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2),
                                     )
            #Get the positions of every joint point and add them to lmList
            for idx, lm in enumerate(hand.landmark):
                #print(idx, lm)
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                #print(idx, cx, cy)
                lmList.append([idx, cx, cy])
    return lmList

def checkRock(jointsPos):
    return jointsPos[tips_of_finger[0]][1]<jointsPos[tips_of_finger[0]-1][1]

def checkScissors(jointsPos):
    return ((jointsPos[tips_of_finger[2]][2])-(jointsPos[tips_of_finger[1]][2]))>100

def checkPaperOrSpock(jointsPos):
    return ((jointsPos[tips_of_finger[0]][2])-(jointsPos[tips_of_finger[2]][2]))>100

def checkSpock(jointsPos):
    return ((jointsPos[tips_of_finger[2]][1])-(jointsPos[tips_of_finger[3]][1]))>50

def checkLizard(jointsPos):
    return ((jointsPos[tips_of_finger[2]][2])-(jointsPos[tips_of_finger[0]][2]))<20

def checkWinnerLoseTie(pc_choice, player_choice):
    wins = 0
    if pc_choice == player_choice:
        cv2.putText(image, f'Pc chose {pc_choice}, you tie!', (740, 50), cv2.FONT_HERSHEY_PLAIN,2.0, (0, 0, 0), 3)
    elif pc_choice in logic[player_choice]:
        cv2.putText(image, f'Pc chose {pc_choice}, you win!', (740, 50), cv2.FONT_HERSHEY_PLAIN,2.0, (0, 0, 0), 3)
        wins += 1
    else:
        cv2.putText(image, f'Pc chose {pc_choice}, you lose!', (740, 50), cv2.FONT_HERSHEY_PLAIN,2.0, (0, 0, 0), 3) 
    return wins

def getChoiceEmoji(jointsPos): 
    player_choice = ''
    if len(jointsPos) != 0:
        if checkRock(jointsPos):
            h, w, c = overLayList[2].shape
            image[0:h,0:w] = overLayList[2]
            player_choice = 'rock'
        elif checkScissors(jointsPos):
            h, w, c = overLayList[3].shape
            image[0:h,0:w] = overLayList[3]
            player_choice = 'scissors'
        elif checkPaperOrSpock(jointsPos):
            if checkSpock(jointsPos):
                h, w, c = overLayList[1].shape
                image[0:h,0:w] = overLayList[1]
                player_choice = 'spock'
            else:
                h, w, c = overLayList[0].shape
                image[0:h,0:w] = overLayList[0]
                player_choice = 'paper'
        elif checkLizard(jointsPos):
            h, w, c = overLayList[4].shape
            image[0:h,0:w] = overLayList[4]
            player_choice = 'lizard'
    return player_choice


overLayList = setImagesPaths("emojis")
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
logic = {
    'scissors': ['paper', 'lizard'],
    'paper': ['rock', 'spock'],
    'rock': ['lizard','scissors'],
    'lizard': ['spock', 'paper'],
    'spock': ['scissors', 'rock']
}
player_choice = ''
tips_of_finger = [4,8,12,16,20]       
last_detected = datetime.now()
pc_choice = ''
record_wins = 0

cap = cv2.VideoCapture(0)
with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands: 
    while cap.isOpened():
        ret, frame = cap.read()
        results, image = overlayExoSkeleton(frame)
        #print(results)
        
        #Save position of all joints in a frame 
        lmList = renderExoSkeleton(results, image)
        
        #Save choice made and display emoji
        player_choice = getChoiceEmoji(lmList) 

        key = cv2.waitKey(5)
        #If 'p' is clicked play game
        if key == 112 and player_choice:
            last_detected = datetime.now()
            pc_choice = random.choice(list(logic.keys()))
            wins = checkWinnerLoseTie(pc_choice, player_choice)
            record_wins += wins
            cv2.putText(image, f'Wins:{record_wins}', (100, 700), cv2.FONT_HERSHEY_TRIPLEX,2.0, (0, 215, 255), 3) 
        #If 'q' is clicked stop the game/camera
        elif key & 0xFF == ord('q'):
            break
        else:
            if (datetime.now() - last_detected).total_seconds() < 2 and player_choice:
                checkWinnerLoseTie(pc_choice, player_choice)
                cv2.putText(image, f'Wins:{record_wins}', (100, 700), cv2.FONT_HERSHEY_TRIPLEX,2.0, (0, 215, 255), 3) 

        cv2.imshow('Hand Tracking', image)
    
cap.release()
cv2.destroyAllWindows()