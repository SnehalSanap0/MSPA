import os
import smtplib
import json
from email.mime.text import MIMEText
from utils import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, ALERT_EMAIL, SLACK_WEBHOOK_URL
import requests

def send_email_alert(subject, body, recipient=None):
    recipient = recipient or ALERT_EMAIL
    if not (SMTP_USER and SMTP_PASS and SMTP_HOST and recipient):
        print('Email alert skipped — SMTP not configured')
        return False

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = SMTP_USER
    msg['To'] = recipient

    try:
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.ehlo()
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(SMTP_USER, [recipient], msg.as_string())
        server.quit()
        print('Email alert sent to', recipient)
        return True
    except Exception as e:
        print('Failed to send email alert:', e)
        return False

def send_slack_alert(text):
    if not SLACK_WEBHOOK_URL:
        print('Slack alert skipped — webhook not configured')
        return False
    try:
        r = requests.post(SLACK_WEBHOOK_URL, json={'text': text}, timeout=5)
        return r.status_code == 200
    except Exception as e:
        print('Failed to send slack alert:', e)
        return False

def notify_down(url, details=''):
    subject = f'🚨 API DOWN: {url}'
    body = f'{url} appears DOWN.\n\nDetails:\n{details}\nTime: {__import__("utils").now_iso()}'
    send_email_alert(subject, body)
    send_slack_alert(body)