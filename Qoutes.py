import requests
from bs4 import BeautifulSoup
import csv

BASE_URL = "http://quotes.toscrape.com"
START_URL = BASE_URL + "/page/1/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

def scrape_quotes():
    quotes = []
    page = 1

    while True:
        url = f"{BASE_URL}/page/{page}/"
        print(f"Scraping {url}...")

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            break

        soup = BeautifulSoup(response.text, "html.parser")
        quote_blocks = soup.select("div.quote")

        if not quote_blocks:
            break

        for quote in quote_blocks:
            text = quote.find("span", class_="text").text.strip()
            author = quote.find("small", class_="author").text.strip()
            tags = [tag.text for tag in quote.select(".tags a.tag")]
            quotes.append({
                "Text": text,
                "Author": author,
                "Tags": ", ".join(tags)
            })

        page += 1

    return quotes

def save_to_csv(quotes, filename="quotes.csv"):
    keys = quotes[0].keys()
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(quotes)
    print(f"\nSaved {len(quotes)} quotes to {filename}")

if __name__ == "__main__":
    quotes = scrape_quotes()
    if quotes:
        save_to_csv(quotes)
