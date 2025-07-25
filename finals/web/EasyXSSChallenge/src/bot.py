from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlencode
import time
import os

FLAG = os.getenv("FLAG")

def admin_bot(params):
    # Step 1: Start headless Chrome
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=options)

    try:
        # Step 2: Visit localhost and set flag cookie
        driver.get("http://localhost:38457/")  # Initial visit required before setting cookies
        driver.add_cookie({"name": "flag", "value": FLAG, "domain": "localhost"})

        # Step 3: Visit render endpoint with params
        target_url = f"http://localhost:38457/render?{params}"
        driver.get(target_url)

        # Let JS run for a few seconds
        time.sleep(3)

    except Exception as e:
        print(f"[!] Bot error: {e}")

    finally:
        driver.quit()
