import cv2
import mediapipe as mp
import time
import numpy as np
import pytesseract
from PIL import ImageGrab
import pyautogui

prev_pressed = 0
cur_pressed = 0

time.sleep(2.0)

mp_draw=mp.solutions.drawing_utils
mp_hand=mp.solutions.hands
mp_style = mp.solutions.drawing_styles

tipIds=[4,8,12,16,20]

video=cv2.VideoCapture(0)

#screen_reader = ImageGrab.grab(bbox=(0, 0, 128, 128))

def get_label(index, hand, results):
    output = None
    for idx, classification in enumerate(results.multi_handedness):
        if classification.classification[0].index == index:
            # Process results
            label = classification.classification[0].label
            score = classification.classification[0].score
            text = '{} {}'.format(label, round(score, 2))

            # Extract Coordinates
            coords = tuple(np.multiply(
                np.array((hand.landmark[mp_hand.HandLandmark.WRIST].x, hand.landmark[mp_hand.HandLandmark.WRIST].y)),
                [640, 480]).astype(int))

            output = text, coords

    return output
with mp_hand.Hands(min_detection_confidence=0.5,
               min_tracking_confidence=0.5) as hands:
    while True:
        keyPressed = False
        break_pressed=False
        jump_pressed=False
        dunk_pressed=False
        accelerator_pressed=False
        key_count=0
        key_pressed=0
        ret,image=video.read()
        image=cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable=False
        results=hands.process(image)
        image.flags.writeable=True
        image=cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        lmList=[]
        text=''
        if results.multi_hand_landmarks:
            for idx, classification in enumerate(results.multi_handedness):
                if classification.classification[0].index == idx:
                    label = classification.classification[0].label
                    text = '{}'.format(label)
                else:
                    label = classification.classification[0].label
                    text = '{}'.format(label)
            for hand_landmark in results.multi_hand_landmarks:
                myHands=results.multi_hand_landmarks[0]
                for id, lm in enumerate(myHands.landmark):
                    h,w,c=image.shape
                    cx,cy= int(lm.x*w), int(lm.y*h)
                    lmList.append([id,cx,cy])
                mp_draw.draw_landmarks(
                    image,
                    hand_landmark,
                    mp_hand.HAND_CONNECTIONS,
                    mp_style.get_default_hand_landmarks_style(),
                    mp_style.get_default_hand_connections_style())
        fingers=[]
        image = cv2.flip(image, 1)
        if len(lmList)!=0:
            if lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
            for id in range(1,5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            total=fingers.count(1)
            if total==4 and text=="Right":
                cv2.rectangle(image, (100, 300), (250, 425), (255, 255, 255), cv2.FILLED)
                cv2.putText(image, "UP", (100, 375), cv2.FONT_HERSHEY_SIMPLEX,
                    2, (0, 0, 255), 5)

                cur_pressed = 1

            elif total==5 and text=="Left":
                cv2.rectangle(image, (400, 300), (650, 425), (255, 255, 255), cv2.FILLED)
                cv2.putText(image, "DOWN", (400, 375), cv2.FONT_HERSHEY_SIMPLEX,
                    2, (0, 255, 0), 5)

                cur_pressed = 2

            elif total==1:
                cv2.rectangle(image, (100, 300), (250, 400), (255, 255, 255), cv2.FILLED)
                cv2.putText(image, "LEFT", (100, 375), cv2.FONT_HERSHEY_SIMPLEX,
                    2, (0, 0, 255), 5)
                if prev_pressed == 1:
                    pyautogui.press('w')
                    cur_pressed = 3
                
            elif total==0:
                cv2.rectangle(image, (400, 300), (600, 425), (255, 255, 255), cv2.FILLED)
                cv2.putText(image, "RIGHT", (400, 375), cv2.FONT_HERSHEY_SIMPLEX,
                    2, (0, 255, 0), 5)

                if prev_pressed == 2:
                    pyautogui.press('s')
                    cur_pressed = 4
                
        prev_pressed = cur_pressed


        
        cv2.imshow("Computer Vision", image)
        k=cv2.waitKey(1)
        if k == ord('q'):
            break
video.release()
cv2.destroyAllWindows()