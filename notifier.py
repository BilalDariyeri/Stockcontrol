import os
import requests
from dotenv import load_dotenv

load_dotenv()

def send_telegram_message(message):
    token = os.getenv("BOT_API")
    chat_ids = os.getenv("CHAT_IDS")

    if not token or not chat_ids:
        print("⚠️ BOT_API veya CHAT_IDS .env dosyasında yok.")
        return

    # Chat ID’leri virgülle ayrılmış string, listeye çeviriyoruz
    chat_id_list = [chat_id.strip() for chat_id in chat_ids.split(",")]

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    for chat_id in chat_id_list:
        payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "HTML"
        }

        try:
            response = requests.post(url, data=payload, timeout=10)
            response.raise_for_status()
            print(f"Telegram mesajı {chat_id} kullanıcısına gönderildi.")
        except requests.exceptions.RequestException as e:
            print(f"Telegram mesajı {chat_id} kullanıcısına gönderilemedi: {e}")

if __name__ == "__main__":
    send_telegram_message("Test mesajı: Telegram bildirim sistemi çoklu chat ID ile çalışıyor!")
