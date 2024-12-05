import os
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://openlibrary.org/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}

# Create directory to save images
SAVE_DIR = "policyaddress"
os.makedirs(SAVE_DIR, exist_ok=True)


def download_image(image_url, save_dir):
    """Download an image and save it locally."""
    try:
        response = requests.get(image_url, headers=HEADERS, stream=True)
        if response.status_code == 200:
            filename = os.path.join(save_dir, os.path.basename(image_url))
            with open(filename, "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"Downloaded: {filename}")
    except Exception as e:
        print(f"Failed to download {image_url}: {e}")


def get_images_from_page(url):
    """Fetch all image URLs from a page."""
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    images = []

    # Find all <img> tags
    img_tags = soup.find_all("img")
    for img in img_tags:
        src = img.get("src")
        if src and src.startswith("/"):
            # Convert relative URL to absolute
            full_url = urljoin(BASE_URL, src)
            images.append(full_url)
        elif src and src.startswith("http"):
            images.append(src)
    return images


def crawl_openlibrary_images(start_url, max_pages=5):
    """Crawl Open Library and download images."""
    page = 1
    next_page_url = start_url
    while next_page_url and page <= max_pages:
        print(f"Crawling page {page}: {next_page_url}")
        images = get_images_from_page(next_page_url)
        for img_url in images:
            if "covers.openlibrary.org" in img_url:  # Only download cover images
                download_image(img_url, SAVE_DIR)

        # Find next page link
        response = requests.get(next_page_url, headers=HEADERS)
        soup = BeautifulSoup(response.text, "html.parser")
        next_page = soup.select_one(".pagination .next a")
        next_page_url = urljoin(BASE_URL, next_page["href"]) if next_page else None
        page += 1


# Start crawling
if __name__ == "__main__":
    crawl_openlibrary_images(BASE_URL, max_pages=10)
