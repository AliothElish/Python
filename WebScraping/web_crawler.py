import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

# Starting URL and visited pages set
start_url = "https://www.info.gov.hk/"
visited_pages = set()


def crawl(url):
    # Check if the page has already been visited
    if url in visited_pages:
        return
    visited_pages.add(url)

    # Fetch the content of the page
    try:
        response = requests.get(url)
        response.encoding = response.apparent_encoding
        response.raise_for_status()
        print(f"Crawling: {url}")
    except requests.RequestException as e:
        print(f"Failed to retrieve {url}: {e}")
        return

    # Parse the page content
    soup = BeautifulSoup(response.text, "html.parser")

    # Example: Print the title of the page
    title = soup.find("title")
    print(f"Title: {title.string if title else 'No title found'}")

    # Find all links and recursively crawl them
    print(soup.find_all("a", href=True))
    for link in soup.find_all("a", href=True):
        next_url = urljoin(url, link["href"])
        if next_url.startswith("https://www.info.gov.hk/"):
            time.sleep(1)  # polite crawling by pausing between requests
            crawl(next_url)


# Start crawling from the start_url
crawl(start_url)
[
    "index.html",
    "policy.html",
    "supplement.html",
    "highlight.html",
    "webcast.html",
    "press.html",
    "multimedia.html",
    "policy.html",
    "supplement.html",
    "highlight.html",
    "webcast.html",
    "press.html",
    "multimedia.html",
    "archive.html",
    "contact.html",
    "text-size.html",
    "",
    "",
    "highlight.html?id=highlight-01",
    "highlight.html?id=highlight-02",
    "highlight.html?id=highlight-03",
    "highlight.html?id=highlight-04",
    "highlight.html?id=highlight-05",
    "highlight.html?id=highlight-06",
    "highlight.html?id=highlight-07",
    "highlight.html?id=highlight-08",
    "",
    "",
    "",
    "notices.html",
    "privacy.html",
    "sitemap.html",
]
