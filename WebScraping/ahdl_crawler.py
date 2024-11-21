import csv
import time
from datetime import datetime, timezone

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://arkhamdb.com"
DECKLISTS_URL = f"{BASE_URL}/decklists/popular"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}
date_now = datetime.now().replace(tzinfo=timezone.utc)
# 设置筛选的目标日期
# target_date = datetime.strptime("2019-04-20", "%Y-%m-%d").replace(tzinfo=timezone.utc)
# target_date = datetime.strptime("2019-09-27", "%Y-%m-%d").replace(tzinfo=timezone.utc)
# target_date = datetime.strptime("2020-10-15", "%Y-%m-%d").replace(tzinfo=timezone.utc)
# target_date = datetime.strptime("2021-06-28", "%Y-%m-%d").replace(tzinfo=timezone.utc)
target_date = datetime.strptime("2022-08-26", "%Y-%m-%d").replace(tzinfo=timezone.utc)
# target_date = datetime.strptime("2023-08-30", "%Y-%m-%d").replace(tzinfo=timezone.utc)
# target_date = datetime.strptime("2024-02-20", "%Y-%m-%d").replace(tzinfo=timezone.utc)
# target_date = datetime.strptime("2024-10-23", "%Y-%m-%d").replace(tzinfo=timezone.utc)


def get_deck_links(page=1):
    """Fetch deck links from a single page."""
    url = f"{DECKLISTS_URL}/{page}"
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")

    # Find deck entries
    deck_entries = soup.select("tbody tr")
    decks = []
    for entry in deck_entries:
        date_str = entry.find("time").get("datetime")
        date_obj = datetime.fromisoformat(date_str)
        if date_obj < target_date:
            continue

        id = entry.find("img").get("src").split(".")[0].split("/")[-1]

        deck_name = entry.find("a", class_="decklist-name").text.strip()

        likes = int(
            entry.find("a", class_="social-icon-like")
            .find("span", class_="num")
            .get_text(strip=True)
        )

        deck_url = BASE_URL + entry.find("a", class_="decklist-name").get("href")

        # 计算平均增长率
        days_existed = (date_now - date_obj).days + 1  # 避免除以零
        avg_likes_per_day = likes / days_existed

        decks.append(
            {
                "id": id,
                "title": deck_name,
                "likes": likes,
                "created_date": date_obj,
                "avg_likes_per_day": avg_likes_per_day,
                "url": deck_url,
            }
        )
    return decks


def get_all_decks(max_pages=10):
    """Fetch all decks by iterating over pages."""
    all_decks = []
    for page in range(1, max_pages + 1):
        print(f"Fetching page {page}...")
        decks = get_deck_links(page)
        if not decks:  # If no more decks are found, stop.
            continue
        all_decks.extend(decks)
        time.sleep(1)  # Polite delay
    return all_decks


# Main script
if __name__ == "__main__":
    # Step 1: Fetch all deck links
    all_decks = get_all_decks(max_pages=1029)
    print(f"Found {len(all_decks)} decks.")

    # Step 2: Sort each deck
    all_decks.sort(key=lambda x: x["avg_likes_per_day"], reverse=True)
    all_decks.sort(key=lambda x: x["id"])
    unique_ids = {deck["id"] for deck in all_decks}

    # Step 3: Output results
    with open("arkhamdb_decks.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "id",
                "title",
                "likes",
                "created_date",
                "avg_likes_per_day",
                "url",
            ],
        )
        writer.writeheader()
        writer.writerows(all_decks)
