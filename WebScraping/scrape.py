import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
}

response = requests.get("https://www.policyaddress.gov.hk/2024/tc/", headers=headers)
response.encoding = response.apparent_encoding
html = response.text
soup = BeautifulSoup(html, "html.parser")
print(soup)
