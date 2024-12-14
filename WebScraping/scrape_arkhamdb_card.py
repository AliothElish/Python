from datetime import datetime, timezone

import pandas as pd
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://arkhamdb.com"
# DECKLISTS_URL = f"{BASE_URL}/decklists/popular"
FIND_URL = f"{BASE_URL}/decklists/find"
FIND = "faction=&cards%5B%5D=01003&author=&name=&sort=likes&packs%5B%5D=1&packs%5B%5D=1-2&packs%5B%5D=76&packs%5B%5D=2&packs%5B%5D=4&packs%5B%5D=5&packs%5B%5D=8&packs%5B%5D=9&packs%5B%5D=10&packs%5B%5D=11&packs%5B%5D=12&packs%5B%5D=13&packs%5B%5D=14&packs%5B%5D=15&packs%5B%5D=16&packs%5B%5D=17&packs%5B%5D=18&packs%5B%5D=20&packs%5B%5D=21&packs%5B%5D=22&packs%5B%5D=23&packs%5B%5D=24&packs%5B%5D=25&packs%5B%5D=26&packs%5B%5D=29&packs%5B%5D=30&packs%5B%5D=31&packs%5B%5D=34&packs%5B%5D=35&packs%5B%5D=36&packs%5B%5D=37&packs%5B%5D=38&packs%5B%5D=40&packs%5B%5D=41&packs%5B%5D=42&packs%5B%5D=43&packs%5B%5D=44&packs%5B%5D=45&packs%5B%5D=52&packs%5B%5D=56&packs%5B%5D=57&packs%5B%5D=58&packs%5B%5D=59&packs%5B%5D=60&packs%5B%5D=61&packs%5B%5D=73&packs%5B%5D=74&packs%5B%5D=79&packs%5B%5D=80&packs%5B%5D=84&packs%5B%5D=85&packs%5B%5D=28&packs%5B%5D=33&packs%5B%5D=39&packs%5B%5D=54&packs%5B%5D=72&packs%5B%5D=47&packs%5B%5D=48&packs%5B%5D=49&packs%5B%5D=50&packs%5B%5D=51&packs%5B%5D=3&packs%5B%5D=6&packs%5B%5D=27&packs%5B%5D=32&packs%5B%5D=46&packs%5B%5D=55&packs%5B%5D=70&packs%5B%5D=77&packs%5B%5D=81&packs%5B%5D=82&packs%5B%5D=92&packs%5B%5D=19&packs%5B%5D=63&packs%5B%5D=64&packs%5B%5D=65&packs%5B%5D=66&packs%5B%5D=67&packs%5B%5D=68&packs%5B%5D=69&packs%5B%5D=7&packs%5B%5D=53&packs%5B%5D=62&packs%5B%5D=71&packs%5B%5D=75&packs%5B%5D=78&packs%5B%5D=83&packs%5B%5D=86&packs%5B%5D=87&packs%5B%5D=88&packs%5B%5D=89&packs%5B%5D=90&packs%5B%5D=91"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
}
TABOO_DATE = datetime.strptime("2022-08-26", "%Y-%m-%d").replace(tzinfo=timezone.utc)
# TABOO_DATE = datetime.strptime("2021-11-19", "%Y-%m-%d").replace(tzinfo=timezone.utc)
# TABOO_DATE = datetime.strptime("2021-06-28", "%Y-%m-%d").replace(tzinfo=timezone.utc)

current_time = datetime.now(timezone.utc)


def fetch_deck_data(max_pages=10):
    """Fetch all deck data up to max_pages."""
    results = []

    for page_num in range(max_pages):
        print(f"Fetching page {page_num + 1}...")
        response = requests.get(f"{FIND_URL}/{page_num + 1}?{FIND}", headers=HEADERS)

        if response.status_code != 200:
            print(f"Failed to fetch page {page_num + 1}: {response.status_code}")
            continue

        html = response.text
        soup = BeautifulSoup(html, "html.parser")

        all_images = soup.findAll("img")
        all_names = soup.findAll("a", attrs={"class": "decklist-name"})
        all_likes = soup.findAll("a", attrs={"class": "social-icon-like"})
        all_times = soup.findAll("time")

        for image, name, like, create_time in zip(
            all_images, all_names, all_likes, all_times
        ):
            time_datetime = datetime.fromisoformat(create_time["datetime"])
            if time_datetime < TABOO_DATE:
                continue

            days_difference = (current_time - time_datetime).days + 1
            if days_difference < 15:  # Filter decks with less than 14 days of existence
                continue

            image_src = image["src"].split("/")[-1].split(".")[0]
            name_string = name.string
            like_num = int(like.find("span", attrs={"class": "num"}).string)

            daily_likes = like_num / days_difference

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


def filter_top_10_per_id(decks):
    """Filter top 10 decks by daily_likes for each unique id using pandas."""
    df = pd.DataFrame(decks)
    # Sort by 'id' and 'daily_likes' descending
    df = df.sort_values(by=["daily_likes"], ascending=[False])

    # Keep only top 10 for each 'id'
    top_10_decks = df  # .groupby("id").head(10)
    return top_10_decks


def save_to_csv(decks, filename="arkhamdb_top_decks.csv"):
    """Save filtered decks to a CSV file using pandas."""
    decks.to_csv(filename, index=False, encoding="utf-8")


if __name__ == "__main__":
    # Fetch and process data
    all_decks = fetch_deck_data(max_pages=29)
    filtered_decks = filter_top_10_per_id(all_decks)
    save_to_csv(filtered_decks, "O'Toole.csv")
    print(f"Saved {len(filtered_decks)} decks to CSV.")
