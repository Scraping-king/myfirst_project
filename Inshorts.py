import requests
from bs4 import BeautifulSoup
import csv

def scrape_inshorts(category="all"):
    url = f"https://inshorts.com/en/read/{category}" if category != "all" else "https://inshorts.com/en/read"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    news_cards = soup.find_all("div", class_="news-card")

    news_data = []
    for card in news_cards:
        try:
            headline = card.find("span", itemprop="headline").text.strip()
            summary = card.find("div", itemprop="articleBody").text.strip()
            news_data.append({
                "Category": category,
                "Headline": headline,
                "Summary": summary
            })
        except Exception as e:
            print("Error parsing a news card:", e)
            continue

    return news_data

def save_to_csv(data, filename="inshorts_news.csv"):
    if not data:
        print("No data to save.")
        return
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Category", "Headline", "Summary"])
        writer.writeheader()
        writer.writerows(data)
    print(f"✅ Saved {len(data)} articles to {filename}")

if __name__ == "__main__":
    # You can change this to "sports", "technology", "business", etc.
    data = scrape_inshorts(category="technology")
    save_to_csv(data)
