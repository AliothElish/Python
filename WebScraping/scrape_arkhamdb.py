import asyncio
import time
from datetime import datetime, timezone

import aiohttp
import pandas as pd
from bs4 import BeautifulSoup

BASE_URL = "https://arkhamdb.com"
DECKLISTS_URL = f"{BASE_URL}/decklists/popular"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
}
TABOO_DATE = datetime.strptime("2022-08-26", "%Y-%m-%d").replace(tzinfo=timezone.utc)
current_time = datetime.now(timezone.utc)


async def fetch_page(session, page_num):
    """Fetch a single page asynchronously."""
    url = f"{DECKLISTS_URL}/{page_num + 1}"
    print(f"Fetching page {page_num + 1}...")
    try:
        async with session.get(url, headers=HEADERS) as response:
            if response.status != 200:
                print(f"Failed to fetch page {page_num + 1}: {response.status}")
                return None
            print(f"Page {page_num + 1} obtained.")
            return await response.text()
    except Exception as e:
        print(f"Error fetching page {page_num + 1}: {e}")
        return None


async def fetch_all_pages(max_pages):
    """Fetch all pages asynchronously."""
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_page(session, page_num) for page_num in range(max_pages)]
        return await asyncio.gather(*tasks)


def parse_page(html):
    """Parse a single page's HTML."""
    if not html:
        return []

    soup = BeautifulSoup(html, "html.parser")
    all_images = soup.findAll("img")
    all_names = soup.findAll("a", attrs={"class": "decklist-name"})
    all_likes = soup.findAll("a", attrs={"class": "social-icon-like"})
    all_times = soup.findAll("time")

    results = []
    for image, name, like, time_element in zip(
        all_images, all_names, all_likes, all_times
    ):
        time_datetime = datetime.fromisoformat(time_element["datetime"])
        if time_datetime < TABOO_DATE:
            continue

        days_difference = (current_time - time_datetime).days + 1
        if days_difference < 15:  # Filter decks with less than 14 days of existence
            continue

        image_src = image["src"].split("/")[-1].split(".")[0]
        name_string = name.string
        like_num = int(like.find("span", attrs={"class": "num"}).string)

        daily_likes = like_num**2 / days_difference

        results.append(
            {
                "id": image_src,
                "name": name_string,
                "likes": like_num,
                "daily_likes": daily_likes,
                "created_at": time_datetime,
                "url": BASE_URL + name["href"],
            }
        )
    return results


async def fetch_deck_data_async(max_pages=10):
    """Fetch all deck data up to max_pages asynchronously."""
    pages = await fetch_all_pages(max_pages)
    results = []
    for html in pages:
        results.extend(parse_page(html))
    return results


def filter_top_10_per_id(decks):
    """Filter top 10 decks by daily_likes for each unique id using pandas."""
    df = pd.DataFrame(decks)
    # Sort by 'id' and 'daily_likes' descending
    df = df.sort_values(by=["id", "daily_likes"], ascending=[True, False])

    # Keep only top 10 for each 'id'
    top_10_decks = df.groupby("id").head(10)
    return top_10_decks


def save_to_csv(decks, filename="arkhamdb_top_decks.csv"):
    """Save filtered decks to a CSV file using pandas."""
    decks.to_csv(filename, index=False, encoding="utf-8")


if __name__ == "__main__":
    start_time = time.time()
    max_pages = 1037
    # Fetch and process data
    all_decks = asyncio.run(fetch_deck_data_async(max_pages=max_pages))
    filtered_decks = filter_top_10_per_id(all_decks)
    save_to_csv(filtered_decks)
    print(f"Saved {len(filtered_decks)} decks to CSV.")
    print(f"Run time: {time.time() - start_time} seconds")
