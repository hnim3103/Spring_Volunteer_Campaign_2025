import cv2
import pytesseract
from PIL import ImageGrab 
import numpy as np 
import pyautogui
import time

pytesseract.pytesseract.tesseract_cmd = r'E:\Python\Tesseract\tesseract.exe'

isEscaped = False

while True: 
    #left, top, right, bottom
    img = ImageGrab.grab(bbox=(970, 260, 1060, 285))
    
    reconized_text = pytesseract.image_to_string(img)
    
    print(reconized_text)
       
    np_img = np.array(img)
    
    cv2.imshow("Screen Capture", np_img)
    
    key = cv2.waitKey(1)
    if key == 27:
        break
cv2.destroyAllWindows()