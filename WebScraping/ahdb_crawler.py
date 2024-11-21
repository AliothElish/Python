from datetime import datetime, timezone

import requests
from bs4 import BeautifulSoup

# 目标URL
url = input("Links: ")

num = "01002"
link = "https://arkhamdb.com/decklists/find?faction=&cards%5B%5D={num}&author=&name=&sort=likes&packs%5B%5D=1&packs%5B%5D=1-2&packs%5B%5D=76&packs%5B%5D=2&packs%5B%5D=4&packs%5B%5D=5&packs%5B%5D=8&packs%5B%5D=9&packs%5B%5D=10&packs%5B%5D=11&packs%5B%5D=12&packs%5B%5D=13&packs%5B%5D=14&packs%5B%5D=15&packs%5B%5D=16&packs%5B%5D=17&packs%5B%5D=18&packs%5B%5D=20&packs%5B%5D=21&packs%5B%5D=22&packs%5B%5D=23&packs%5B%5D=24&packs%5B%5D=25&packs%5B%5D=26&packs%5B%5D=29&packs%5B%5D=30&packs%5B%5D=31&packs%5B%5D=34&packs%5B%5D=35&packs%5B%5D=36&packs%5B%5D=37&packs%5B%5D=38&packs%5B%5D=40&packs%5B%5D=41&packs%5B%5D=42&packs%5B%5D=43&packs%5B%5D=44&packs%5B%5D=45&packs%5B%5D=52&packs%5B%5D=56&packs%5B%5D=57&packs%5B%5D=58&packs%5B%5D=59&packs%5B%5D=60&packs%5B%5D=61&packs%5B%5D=73&packs%5B%5D=74&packs%5B%5D=79&packs%5B%5D=80&packs%5B%5D=84&packs%5B%5D=85&packs%5B%5D=28&packs%5B%5D=33&packs%5B%5D=39&packs%5B%5D=54&packs%5B%5D=72&packs%5B%5D=47&packs%5B%5D=48&packs%5B%5D=49&packs%5B%5D=50&packs%5B%5D=51&packs%5B%5D=3&packs%5B%5D=6&packs%5B%5D=27&packs%5B%5D=32&packs%5B%5D=46&packs%5B%5D=55&packs%5B%5D=70&packs%5B%5D=77&packs%5B%5D=81&packs%5B%5D=82&packs%5B%5D=19&packs%5B%5D=63&packs%5B%5D=64&packs%5B%5D=65&packs%5B%5D=66&packs%5B%5D=67&packs%5B%5D=68&packs%5B%5D=69&packs%5B%5D=7&packs%5B%5D=53&packs%5B%5D=62&packs%5B%5D=71&packs%5B%5D=75&packs%5B%5D=78&packs%5B%5D=83&packs%5B%5D=86&packs%5B%5D=87&packs%5B%5D=88&packs%5B%5D=89&packs%5B%5D=90&packs%5B%5D=91"
https://arkhamdb.com/decklists/find?faction=&cards%5B%5D=01006&author=&name=&sort=likes&packs%5B%5D=1&packs%5B%5D=1-2&packs%5B%5D=76&packs%5B%5D=2&packs%5B%5D=4&packs%5B%5D=5&packs%5B%5D=8&packs%5B%5D=9&packs%5B%5D=10&packs%5B%5D=11&packs%5B%5D=12&packs%5B%5D=13&packs%5B%5D=14&packs%5B%5D=15&packs%5B%5D=16&packs%5B%5D=17&packs%5B%5D=18&packs%5B%5D=20&packs%5B%5D=21&packs%5B%5D=22&packs%5B%5D=23&packs%5B%5D=24&packs%5B%5D=25&packs%5B%5D=26&packs%5B%5D=29&packs%5B%5D=30&packs%5B%5D=31&packs%5B%5D=34&packs%5B%5D=35&packs%5B%5D=36&packs%5B%5D=37&packs%5B%5D=38&packs%5B%5D=40&packs%5B%5D=41&packs%5B%5D=42&packs%5B%5D=43&packs%5B%5D=44&packs%5B%5D=45&packs%5B%5D=52&packs%5B%5D=56&packs%5B%5D=57&packs%5B%5D=58&packs%5B%5D=59&packs%5B%5D=60&packs%5B%5D=61&packs%5B%5D=73&packs%5B%5D=74&packs%5B%5D=79&packs%5B%5D=80&packs%5B%5D=84&packs%5B%5D=85&packs%5B%5D=28&packs%5B%5D=33&packs%5B%5D=39&packs%5B%5D=54&packs%5B%5D=72&packs%5B%5D=47&packs%5B%5D=48&packs%5B%5D=49&packs%5B%5D=50&packs%5B%5D=51&packs%5B%5D=3&packs%5B%5D=6&packs%5B%5D=27&packs%5B%5D=32&packs%5B%5D=46&packs%5B%5D=55&packs%5B%5D=70&packs%5B%5D=77&packs%5B%5D=81&packs%5B%5D=82&packs%5B%5D=19&packs%5B%5D=63&packs%5B%5D=64&packs%5B%5D=65&packs%5B%5D=66&packs%5B%5D=67&packs%5B%5D=68&packs%5B%5D=69&packs%5B%5D=7&packs%5B%5D=53&packs%5B%5D=62&packs%5B%5D=71&packs%5B%5D=75&packs%5B%5D=78&packs%5B%5D=83&packs%5B%5D=86&packs%5B%5D=87&packs%5B%5D=88&packs%5B%5D=89&packs%5B%5D=90&packs%5B%5D=91

# 设置筛选的目标日期
# target_date = datetime.strptime("2019-04-20", "%Y-%m-%d").replace(tzinfo=timezone.utc)
# target_date = datetime.strptime("2019-09-27", "%Y-%m-%d").replace(tzinfo=timezone.utc)
# target_date = datetime.strptime("2020-10-15", "%Y-%m-%d").replace(tzinfo=timezone.utc)
# target_date = datetime.strptime("2021-06-28", "%Y-%m-%d").replace(tzinfo=timezone.utc)
target_date = datetime.strptime("2022-08-26", "%Y-%m-%d").replace(tzinfo=timezone.utc)
# target_date = datetime.strptime("2023-08-30", "%Y-%m-%d").replace(tzinfo=timezone.utc)
# target_date = datetime.strptime("2024-02-20", "%Y-%m-%d").replace(tzinfo=timezone.utc)
# target_date = datetime.strptime("2024-10-23", "%Y-%m-%d").replace(tzinfo=timezone.utc)

# 发送HTTP请求
response = requests.get(url)

if response.status_code == 200:
    # 解析HTML内容
    soup = BeautifulSoup(response.content, "html.parser")

    # 示例：获取卡组信息
    deck_data = []
    decks = soup.find_all("article")  # 假设卡组被封装在 div 中
    for deck in decks:
        try:
            # 假设喜欢数在某个 span 中
            likes = int(
                deck.find("a", class_="social-icon-like")
                .find("span", class_="num")
                .get_text(strip=True)
            )
            # 假设日期在某个 time 标签中
            date_str = deck.find("time").get("datetime")
            date_obj = datetime.fromisoformat(date_str)
            if date_obj < target_date:
                continue

            # 假设链接在某个 a 标签中
            link = deck.find("a", class_="decklist-name").get("href")
            full_link = f"https://arkhamdb.com{link}"

            # 计算平均增长率
            days_existed = (datetime.now(date_obj.tzinfo) - date_obj).days
            days_existed = max(days_existed, 1)  # 避免除以零
            avg_likes_per_day = likes / days_existed

            # 存储数据
            deck_data.append(
                {
                    "likes": likes,
                    "date": date_obj,
                    "days_existed": days_existed,
                    "avg_likes_per_day": avg_likes_per_day,
                    "link": full_link,
                }
            )
        except Exception as e:
            print(f"解析卡组时出错: {e}")

    # 按平均增加数排序
    deck_data.sort(key=lambda x: x["avg_likes_per_day"], reverse=True)

    # 输出增长最快的卡组
    if deck_data:
        for deck in deck_data:
            print(f"增长最快的卡组链接: {deck['link']}")
            print(
                f"喜欢数: {deck['likes']}, 日期: {deck['date']}, "
                f"平均每天增加: {deck['avg_likes_per_day']:.2f}"
            )
    else:
        print("未找到任何卡组信息。")
else:
    print(f"请求失败，状态码: {response.status_code}")
