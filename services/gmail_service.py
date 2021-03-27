from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import mimetypes


scopes = ["https://www.googleapis.com/auth/gmail.compose"]
email = "j.robson1065@gmail.com"


def create_service():
    creds = None
    if os.path.exists("./sec/token.json"):
        creds = Credentials.from_authorized_user_file(
            "./sec/token.json", scopes)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "./sec/credentials.json", scopes)
            creds = flow.run_local_server(port=0)
        with open("./sec/token.json", "w") as token:
            token.write(creds.to_json())

    service = build("gmail", "v1", credentials=creds)

    return service


def create_message(file, url):
    message_text = "You daily inspirational image and translation has been posted successfully. Check it out here " + url
    message = MIMEMultipart()
    message["to"] = email
    message["from"] = email
    message["subject"] = "Daily Inspirational Quote"
    msg = MIMEText(message_text)
    message.attach(msg)
    
    content_type, encoding = mimetypes.guess_type(file)
    content_type = 'application/octet-stream'
    main_type, sub_type=content_type.split('/', 1)
    fp = open(file, 'rb')
    msg = MIMEImage(fp.read(), _subtype=sub_type)
    fp.close()
    filename = os.path.basename(file)
    msg.add_header('Content-Disposition', 'attachment', filename=filename)
    message.attach(msg)

    return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}


def send_email(file, url):
    service = create_service()
    message = create_message(file, url)
    message = (service.users().messages().send(
        userId="me", body=message).execute())
    return message
