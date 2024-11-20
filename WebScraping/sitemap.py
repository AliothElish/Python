import ssl
import urllib.request as rq
from urllib.parse import urljoin

sitemap_url = urljoin("https://vuejs.org/api", "/sitemap.xml")
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/"
}
http = rq.Request(url=sitemap_url, headers=headers)

ctx = ssl.create_default_context()
http_run = rq.urlopen(http, context=ctx)
print(http_run.read())
