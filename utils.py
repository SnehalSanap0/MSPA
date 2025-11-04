import os
from datetime import datetime
from dotenv import load_dotenv


load_dotenv()


def now_iso():
    return datetime.utcnow().isoformat() + 'Z'


# Environment helpers
SMTP_HOST = os.getenv('SMTP_HOST')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
SMTP_USER = os.getenv('SMTP_USER')
SMTP_PASS = os.getenv('SMTP_PASS')
ALERT_EMAIL = os.getenv('ALERT_EMAIL')
SLACK_WEBHOOK_URL = os.getenv('SLACK_WEBHOOK_URL')