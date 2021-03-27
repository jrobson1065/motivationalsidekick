import time
import schedule
from services.gmail_service import send_email
from services.web_scrape_service import find_img
from services.lang_service import rand_lang, translate, check_words
from string import ascii_letters as letters
from services.automation_service import post_to_fb
from services.ocr_service import read_ss
import os


def quote_info(lang):
    text = ""
    while True:
        text = find_img(lang)
        text = translate(text)
        try:
            if len(text.split(" ")) < 1:
                print("Text not long enough")
                continue
            if not any(t in letters for t in text):
                print("No words found")
                continue
        except:
            continue
        text = check_words(text)
        if not text:
            continue
        else:
            return text


def verify_screenshot(quote):
    quote = quote.split(" ")
    text = read_ss()
    if not text:
        print("Error: Cannot find screenshot.")
    text = "".join(text)
    text = text.replace("\n", " ")
    text = text.split(" ")
    check = sum(w in text for w in quote)

    confidence = check / len(quote) * 100
    if confidence > 80:
        return True
    return False

def remove_previous_ss():
    try:
        if os.path.exists("temp-ss.png"):
            os.remove("temp-ss.png")
    except:
        print("temp-img not found in local directory")


def main():
    lang = rand_lang()
    quote = quote_info(lang)
    quote = "Translation: {} with {}% confidence. Provided by automated Python application written by John Robson.".format(
        quote[0], quote[1])

    remove_previous_ss()
    url = post_to_fb(quote)
    check = verify_screenshot(quote)
    if check:
        img = "/Users/jstar/motivationalsidekick/temp-ss.png"
        send_email(img, url)


if __name__ == "__main__":
    main()
    # schedule.every().day.at("9:00").do(main)

    # while True:
    #   schedule.run_pending()
    #   time.sleep(1)
