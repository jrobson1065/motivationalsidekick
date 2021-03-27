from selenium import webdriver
import base64
from glob import glob
from sec.secrets import pw

from time import sleep

pw = base64.b64decode(pw)
email = "j.robson1065@gmail.com"

def post_to_fb(quote):
    path = glob("temp-img.*")
    ipath = "/Users/jstar/motivationalsidekick/{}".format(path[0])
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    browser = webdriver.Chrome(
        "/Users/jstar/Downloads/chromedriver", chrome_options=chrome_options)
    browser.get("http://mbasic.facebook.com")
    username = browser.find_element_by_id("m_login_email")
    password = browser.find_element_by_name("pass")
    submit = browser.find_element_by_name("login")
    username.send_keys(email)
    password.send_keys(pw.decode("utf-8"))
    submit.click()
    submit = browser.find_element_by_xpath('//a[@target="_self"]')
    submit.click()
    post_box = browser.find_element_by_name("xc_message")
    post_box.send_keys(quote)
    img_btn = browser.find_element_by_xpath("//input[@value='Photo']")
    img_btn.click()
    file_btn = browser.find_element_by_xpath("//input[@name='file1']")
    file_btn.send_keys(ipath)
    preview_btn = browser.find_element_by_xpath("//input[@value='Preview']")
    preview_btn.click()
    post_box = browser.find_element_by_name("view_post")
    post_box.click()
    profile_btn = browser.find_element_by_css_selector("nav a:nth-of-type(2)")
    profile_btn.click()
    profile_btn = browser.find_element_by_css_selector("article:first-of-type footer div:nth-of-type(2) > a:nth-of-type(4)")
    profile_btn.click()
    profile_btn = browser.find_element_by_css_selector("body > div:first-child")
    profile_btn.screenshot('temp-ss.png')
    url = browser.current_url
    browser.quit()
    
    return url
