from email.mime.text import MIMEText
import requests
from bs4 import BeautifulSoup
import random
from selenium import webdriver
import time
import base64
import schedule
from gmail_service import main

pw = base64.b64decode("YnJpdG5leTIy").decode("utf-8")
email = "j.robson1065@gmail.com"

def get_quote():
    url = "https://www.oberlo.com/blog/motivational-quotes"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    quotes = soup.select(".single-post ol li span")
    return random.choice(quotes).text

def post():
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
    password.send_keys(pw)
    submit.click()
    submit = browser.find_element_by_xpath('//a[@target="_self"]')
    submit.click()
    post_box = browser.find_element_by_name("xc_message")
    post_box.send_keys(quote)
    post_box = browser.find_element_by_name("view_post")
    post_box.click()

    browser.quit()
    
def create_message(sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}
    
def send_message(service, user_id, message):
        message = (service.users().messages().send(userId=user_id, body=message)
                .execute())
        print('Message Id: %s' % message['id'])
        return message

quote = get_quote()

def run():
    post()
    email_msg = create_message(email, email, "Daily Motivational Quote", quote)
    service = main()
    send_message(service, "me", email_msg)

schedule.every().day.at("9:00").do(run)

while 1:
    schedule.run_pending()
    time.sleep(1)
