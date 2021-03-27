import requests
from bs4 import BeautifulSoup
import random
from services.ocr_service import read_image
from services.lang_service import translate_to


def read_rand_img(imgs):
    try:
        img = random.choice(imgs)
        link = img["src"]

        text = read_image(link)

        if not text or is_null(text):
            try:
                imgs.remove(img)
            except:
                print("Image cannot be removed from queue. The image may not exist.")
            finally:
                if len(imgs) > 0:
                    read_rand_img(imgs)
                else:
                    return False
        else:
            return text
    except:
        print("Out of images. Searching for more options.")
        return False


def is_null(text):
    return False if True in [x != " " for x in text] else True


def find_img(lang):
    text = "inspirational quotes " + lang
    search_terms = translate_to(text, lang)
    search_terms = search_terms.split(" ")
    search_terms = "+".join(search_terms)
    url = f"https://google.com/images?q={search_terms}+white+background&tbm=isch"

    page = requests.get(url)
    content = BeautifulSoup(page.content, "html.parser")
    
    imgs = content.select("img")
    
    i = len(imgs) - 1
    while i >= 0:
        try:
            if "encrypted" not in str(imgs[i]):
                imgs.remove(imgs[i])
        except:
            imgs.remove(imgs[i])
            continue
        finally:
            i -= 1

    text = read_rand_img(imgs)
    if text == False or text == "" or text is None:
        find_img(lang)
    return text


def scrape_page(url, trans):

    page = requests.get(url)
    content = BeautifulSoup(page.content, "html.parser")

    imgs = content.select("img")

    i = len(imgs) - 1
    while i >= 0:
        try:
            if "quote" not in imgs[i]["alt"].lower() and "http" not in str(imgs[i]) and \
            trans not in imgs[i]["alt"].lower():
                imgs.remove(imgs[i])
            i -= 1
        except:
            i -= 1

    if len(imgs) == 0 or imgs is None or imgs == []:
        return False

    return imgs