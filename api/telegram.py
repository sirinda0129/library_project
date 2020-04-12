import os
import requests
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
URL = "https://api.telegram.org/bot" + TELEGRAM_TOKEN

def send_telegram(chat_id):
    text = f'На проверку добавлена новая ссылка'
    method = URL + "/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": 'HTML'
    }
    r = requests.post(method, json=data, timeout=5)
    if r.status_code != 200:
        raise Exception(f"Error: {r.status_code} -  {r.text}")
