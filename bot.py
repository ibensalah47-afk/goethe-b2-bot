import os
import requests
import time
from datetime import datetime

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

URL = "https://www.goethe.de/ins/dz/de/spr/prf/gzb1.cfm"

def send_message(message):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("Missing Telegram configuration")
        return

    api = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(api, data={
        "chat_id": CHAT_ID,
        "text": message
    }, timeout=20)

def check_registration():
    try:
        response = requests.get(URL, timeout=30)
        response.raise_for_status()
        page = response.text.lower()

        keywords = [
            "anmeldung",
            "registrierung",
            "b2"
        ]

        if any(word in page for word in keywords):
            send_message(
                "تم العثور على كلمات مرتبطة بالتسجيل. "
                "افتح الموقع الرسمي وتحقق من توفر المواعيد:\n" + URL
            )

        print(datetime.now(), "Page checked")

    except Exception as error:
        print("Error:", error)

if __name__ == "__main__":
    while True:
        check_registration()
        time.sleep(1800)
