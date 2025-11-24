import aiohttp
import time
import asyncio
from aiohttp_socks import ProxyConnector

import requests
N = 100
print(f'Making {N} tmpdirs')

TOR_PROXY = 'socks5h://127.0.0.1:9050'
ONION_BASE = 'http://2zo4u6agf52klaylsf2ytqyvf7ev4r4kpdhhdxvods3c6owbaobfazid.onion/'

async def async_requests_example():
    print("=== Method 1: AsyncIO + aiohttp (via Tor) ===")

    urls = []
    
    for i in range(N):
        urls.append(f"{ONION_BASE}sandbox?method=mktempdir&args=..")

    async def fetch(session, url):
        start_time = time.time()
        try:
            if 'delay' in url:
                delay = int(url.split('delay=')[1])
                await asyncio.sleep(delay / 100)
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

    return results

# asyncio.run(async_requests_example())

r = requests.get(f"{ONION_BASE}list_users", proxies={'http': TOR_PROXY, 'https': TOR_PROXY})
print(r.text[:50])
print(r.status_code)