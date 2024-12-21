import cv2
import pytesseract
from PIL import ImageGrab 
import numpy as np 
import pyautogui

pytesseract.pytesseract.tesseract_cmd = r'E:\Python\Tesseract\tesseract.exe'

while True: 
    #left, top, right, bottom
    img = ImageGrab.grab(bbox=(970, 260, 1060, 285))
    
    reconized_text = pytesseract.image_to_string(img)
    
    print(reconized_text)
    
    #if reconized_text >= "01:00:00":
    #    pyautogui.press('esc')
       