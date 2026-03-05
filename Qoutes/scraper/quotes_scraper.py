import requests
from bs4 import BeautifulSoup
import csv

BASE_URL = "http://quotes.toscrape.com"

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
            print("No more pages found.")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        quote_blocks = soup.select("div.quote")

        if not quote_blocks:
            print("No quotes found. Ending scrape.")
            break

        for quote in quote_blocks:
            text = quote.select_one("span.text").get_text(strip=True)
            author = quote.select_one("small.author").get_text(strip=True)
            tags = [tag.get_text(strip=True) for tag in quote.select(".tags a.tag")]

            quotes.append({
                "Text": text,
                "Author": author,
                "Tags": ", ".join(tags)
            })

        page += 1

    return quotes


def save_to_csv(quotes, filename="quotes.csv"):
    if not quotes:
        print("No quotes to save.")
        return

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=quotes[0].keys())
        writer.writeheader()
        writer.writerows(quotes)

    print(f"\nSaved {len(quotes)} quotes to {filename}")


if __name__ == "__main__":
    quotes = scrape_quotes()
    save_to_csv(quotes)