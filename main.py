import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pygame
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
from notifier import send_telegram_message
from scraperHelpers import check_stock_zara, check_stock_bershka

load_dotenv()

pygame.mixer.init()
cart_status = {}  # Her url için stok bildirimi durumu

while True:
    # Döngü başında güncel ürün listesini oku
    with open("products.json", "r") as f:
        config = json.load(f)

    urls_to_check = config["urls"]

    # Yeni eklenen ürünleri takip için cart_status güncelle
    for item in urls_to_check:
        if item["url"] not in cart_status:
            cart_status[item["url"]] = False

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(
        "--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        for item in urls_to_check:
            url = item["url"]
            store = item["store"]
            sizes_to_check = item.get("sizes", [])

            if cart_status.get(url, False):
                print(f"[INFO] {url} için stok zaten tespit edildi, atlandı.")
                continue

            try:
                driver.get(url)
                print(f"Checking URL: {url}")

                if store == "zara":
                    size_in_stock = check_stock_zara(driver, sizes_to_check)
                elif store == "bershka":
                    size_in_stock = check_stock_bershka(driver, sizes_to_check)
                else:
                    size_in_stock = None
                    print(f"[WARN] Desteklenmeyen mağaza: {store}")

                if size_in_stock:
                    message = f"🛍️ {size_in_stock} BEDENİN TAMAM CANIM DİDEMMM ÇOK GÜZEL OLACAGINA EMİNİMM !!!!\nLink: {url}"
                    print(f"[ALERT] {message}")
                    pygame.mixer.music.load('Crystal.mp3')
                    pygame.mixer.music.play()
                    send_telegram_message(message)
                    cart_status[url] = True
                else:
                    print(f"[INFO] {url} için stok bulunamadı: {', '.join(sizes_to_check)}.")

            except Exception as e:
                print(f"[ERROR] {url} ile ilgili hata: {e}")

    finally:
        driver.quit()

    # Uyku süresi sabit: 60 saniye = 1 dakika
    sleep_time = 15
    print(f"Uyku süresi: {sleep_time // 60} dakika, {sleep_time % 60} saniye.")
    time.sleep(sleep_time)
