import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
import logging
import time
import asyncio

load_dotenv()

SMTP_SERVER = 'smtp.gmail.com'  
SMTP_PORT = 587 
EMAIL_USERNAME =  os.environ.get("EMAIL_USERNAME")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
MY_EMAIL = os.environ.get("MY_EMAIL")

def sendEmail(message : str):
    message = MIMEText('Messdfvdhnsage') 
    start_time = time.perf_counter()  
    message['Subject'] = 'Probo Trading'
    message['From'] = EMAIL_USERNAME
    message['To'] = MY_EMAIL

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
            server.sendmail(EMAIL_USERNAME, MY_EMAIL, message.as_string())
    except smtplib.SMTPException as e:
        print(f"Error sending email: {e}")
    finally:
        end_time = time.perf_counter() 
        execution_time = end_time - start_time
        print(f"Email sent in {execution_time:.4f} seconds")  


