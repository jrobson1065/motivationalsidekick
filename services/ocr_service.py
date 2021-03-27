import cv2
import pytesseract
from skimage import io
import requests
import os
from glob import glob
from PIL import Image
import re


def remove_last_img():
    temp_img = glob("temp-img.*")
    try:
        if os.path.exists(temp_img[0]):
            os.remove(temp_img[0])
    except:
        print("temp-img not found in local directory")


def write_new_img(url):
    try:
        page = requests.get(url)

        f_ext = os.path.splitext(url)[-1]
        if f_ext is None or f_ext == "":
            f_ext = ".jpg"
        f_name = 'temp-img{}'.format(f_ext)
        with open(f_name, 'wb') as f:
            f.write(page.content)
    except:
        print("Cannot fetch image from URL")


def is_corrupted():
    try:
        t_img = glob("temp-img.*")[0]
        try:
            img = Image.open("{}".format(t_img))
            img.verify()
            return False
        except:
            print("The downloaded image may be corrupted. Searching for a new image.")
            return True
    except:
        print("temp-img not found in local directory")
        return False


def pull_text():
    try:
        image = io.imread("temp-img.jpg")
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        text = list(pytesseract.image_to_string(image))
    except:
        return False
    if len(text) > 0:
        i = 0
        for i in range(len(text)-1):
            if text[i] == "\n":
                text[i] = " "
            i += 1
    text.pop()
    try:
        if text[len(text) - 1] == " ":
            text.pop()
    except:
        print("No errors found")
    text = "".join(text)
    
    return re.sub(" +", " ", text)


def read_image(url):
    remove_last_img()
    write_new_img(url)

    if is_corrupted():
        return False

    return pull_text()

def read_ss():
    try:
        image = io.imread("temp-ss.png")
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return list(pytesseract.image_to_string(image))
    except:
        return False