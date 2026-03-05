# amazon_search_scraper_playwright.py

from playwright.sync_api import sync_playwright
import pandas as pd
import time
import random
from datetime import datetime


class AmazonSearchScraper:

    def __init__(self, keyword):
        self.keyword = keyword
        self.base_url = f"https://www.amazon.com/s?k={keyword.replace(' ', '+')}"
        self.results = []

    def scrape_page(self, page):
        print("Scraping current page...")

        page.wait_for_selector("div.s-result-item", timeout=60000)
        products = page.query_selector_all("div.s-result-item[data-component-type='s-search-result']")

        for product in products:
            try:
                title_el = product.query_selector("h2 span")
                title = title_el.inner_text().strip() if title_el else "N/A"

                price_whole = product.query_selector(".a-price-whole")
                price_fraction = product.query_selector(".a-price-fraction")

                if price_whole:
                    price = price_whole.inner_text()
                    if price_fraction:
                        price += "." + price_fraction.inner_text()
                else:
                    price = "N/A"

                rating_el = product.query_selector(".a-icon-alt")
                rating = rating_el.inner_text().strip() if rating_el else "N/A"

                review_el = product.query_selector(".a-size-base")
                reviews = review_el.inner_text().strip() if review_el else "N/A"

                link_el = product.query_selector("h2 a")
                link = "https://www.amazon.com" + link_el.get_attribute("href") if link_el else "N/A"

                self.results.append({
                    "title": title,
                    "price": price,
                    "rating": rating,
                    "reviews": reviews,
                    "url": link
                })

            except Exception:
                continue

    def go_to_next_page(self, page):
        next_button = page.query_selector("a.s-pagination-next")
        if next_button and "s-pagination-disabled" not in next_button.get_attribute("class"):
            next_button.click()
            time.sleep(random.uniform(3, 5))
            return True
        return False

    def run(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            )
            page = context.new_page()

            print(f"Opening search page for: {self.keyword}")
            page.goto(self.base_url, timeout=60000)

            while True:
                self.scrape_page(page)

                print(f"Total products scraped so far: {len(self.results)}")

                has_next = self.go_to_next_page(page)
                if not has_next:
                    print("No more pages found.")
                    break

            browser.close()

        self.save_to_csv()

    def save_to_csv(self):
        filename = f"amazon_{self.keyword.replace(' ','_')}_{datetime.now().strftime('%Y%m%d')}.csv"
        df = pd.DataFrame(self.results)
        df.to_csv(filename, index=False)
        print(f"\n✅ Data saved to {filename}")


if __name__ == "__main__":
    keyword = input("Enter product keyword to search: ")
    scraper = AmazonSearchScraper(keyword)
    scraper.run()