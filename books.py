| books.py | Books to Scrape | Title, Price, Rating, Availability |
import requests
from bs4 import BeautifulSoup
import csv

BASE_URL = "http://books.toscrape.com/"
START_URL = BASE_URL + "catalogue/page-1.html"

headers = {
    "User-Agent": "Mozilla/5.0"
}

def get_rating(star_class):
    ratings = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }
    for rating in ratings:
        if rating in star_class:
            return ratings[rating]
    return None

def scrape_books():
    books = []
    page = 1

    while True:
        url = f"{BASE_URL}catalogue/page-{page}.html"
        print(f"Scraping {url}...")

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            break  # No more pages

        soup = BeautifulSoup(response.text, "html.parser")
        book_items = soup.select("article.product_pod")

        for book in book_items:
            title = book.h3.a["title"]
            price = book.select_one("p.price_color").text.strip()
            rating_class = book.select_one("p.star-rating")["class"]
            rating = get_rating(rating_class)
            availability = book.select_one("p.instock.availability").text.strip()

            books.append({
                "Title": title,
                "Price": price,
                "Rating": rating,
                "Availability": availability
            })

        page += 1

    return books

def save_to_csv(books, filename="books.csv"):
    keys = books[0].keys()
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(books)
    print(f"\nSaved {len(books)} books to {filename}")

if __name__ == "__main__":
    books = scrape_books()
    if books:
        save_to_csv(books)
