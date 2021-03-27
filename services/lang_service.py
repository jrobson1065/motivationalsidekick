import requests
import random
from bs4 import BeautifulSoup
from google_trans_new import google_translator 
import googletrans
import enchant
import difflib

# def rand_lang():
#     url = "https://cloud.google.com/translate/docs/languages"
#     content = BeautifulSoup(requests.get(url).content, "html.parser")
#     languages = content.select("tr td:first-child")
#     return random.choice(languages).text.split("(")[0]

class Trans:
    __instance = None

    @classmethod
    def get_instance(self):
        if self.__instance is None:
            self.__instance = google_translator()
        return self.__instance

def get_translator():
    return Trans().get_instance()

def rand_lang():
    langs = ["english", "french", "spanish", "italian", "portuguese", "german"]
    return random.choice(langs)


def convert_code_to_lang(code):
    library = googletrans.LANGUAGES
    return library[code.lower()]


def convert_lang_to_code(lang):
    library = googletrans.LANGUAGES
    return list(library.keys())[list(library.values()).index(lang.lower())]


def translate(text):
    translator = get_translator()
    code = translator.detect(text)[0]
    if code == "en":
        return text

    return translator.translate(text, lang_tgt="en")


def create_dict(code):
    try:
        return enchant.Dict(code)
    except:
        return enchant.Dict("en_US")


def check_words(text):
    translator = get_translator()
    code = translator.detect(text)[0]
    dictionary = create_dict(code)
    text = text.split(" ")
    for w in text:
        if w != "" and w != " " and w is not None:
            if not dictionary.check(w):
                text[text.index(w)] = autocorrect(dictionary, w)

    text = check_translation(text)
    accuracy = check_accuracy(text)

    
    if accuracy > 70:
       return " ".join(text), round(accuracy)
    else:
       return False


def autocorrect(d, word):
    best_words = []
    best_ratio = 0
    a = set(d.suggest(word))
    for b in a:
        tmp = difflib.SequenceMatcher(None, word, b).ratio()
        if tmp > best_ratio:
            best_words = [b]
            best_ratio = tmp
        elif tmp == best_ratio:
            best_words.append(b)

    try:
        match = best_words[0]
    except:
        match = ""

    return match


def check_translation(text):
    d = create_dict("en")
    for w in text:
        try:
            if not d.check(w):
                text[text.index(w)] = "*"
        except:
            print("Empty string not translated.")
    return text


def check_accuracy(text):
    d = create_dict("en")
    t_count = sum([bool(d.check(w)) for w in text if w != "" and w != "*"])
    return t_count / len(text) * 100

def translate_to(text, lang):
    translator = get_translator()
    if len(lang) > 3:
        code = convert_lang_to_code(lang)
    else:
        code = lang
    return translator.translate(text, lang_tgt=code)