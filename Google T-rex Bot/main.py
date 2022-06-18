import time
import pyautogui
from PIL import Image, ImageOps
from website_control import Trex
import numpy as np

trex = Trex()
time.sleep(4)
pyautogui.press("up")

def get_white_pixel_count():
    pyautogui.screenshot("screenshot.png", region=(370, 380, 250, 90))
    reference_img = Image.open("screenshot.png")
    grayImage = ImageOps.grayscale(reference_img)
    img_array = np.array(grayImage.getcolors())
    pixel_count = 0
    for i in grayImage.getcolors():
        if i[1] == 247:
            pixel_count = i[0]
    print(pixel_count)
    return pixel_count

while True:
    if get_white_pixel_count() < 21200:
        time.sleep(0.15)
        pyautogui.press("up")













