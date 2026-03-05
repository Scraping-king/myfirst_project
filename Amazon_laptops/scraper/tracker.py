# main.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import random
from datetime import datetime


class AmazonFullScraper:

    def __init__(self):
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )

        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)
        self.products = []

    def search_product(self, keyword):
        self.driver.get("https://www.amazon.com")
        time.sleep(random.uniform(2, 4))

        search_box = self.wait.until(
            EC.presence_of_element_located((By.ID, "twotabsearchtextbox"))
        )
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.RETURN)

        time.sleep(random.uniform(3, 5))

    def scrape_current_page(self):
        items = self.driver.find_elements(By.CSS_SELECTOR, "div.s-result-item")

        for item in items:
            try:
                title = item.find_element(By.CSS_SELECTOR, "h2 a span").text
            except:
                title = "N/A"

            try:
                price_whole = item.find_element(By.CSS_SELECTOR, ".a-price-whole").text
                price_fraction = item.find_element(By.CSS_SELECTOR, ".a-price-fraction").text
                price = f"{price_whole}.{price_fraction}"
            except:
                price = "N/A"

            try:
                rating = item.find_element(By.CSS_SELECTOR, ".a-icon-alt").text
            except:
                rating = "N/A"

            try:
                link = item.find_element(By.CSS_SELECTOR, "h2 a").get_attribute("href")
            except:
                link = "N/A"

            if title != "N/A":
                self.products.append({
                    "title": title,
                    "price": price,
                    "rating": rating,
                    "link": link,
                    "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })

    def go_to_next_page(self):
        try:
            next_button = self.driver.find_element(By.CSS_SELECTOR, "a.s-pagination-next")
            next_button.click()
            time.sleep(random.uniform(3, 5))
            return True
        except:
            return False

    def scrape_all_pages(self, keyword, max_pages=5):
        self.search_product(keyword)

        page = 1
        while page <= max_pages:
            print(f"Scraping page {page}...")
            self.scrape_current_page()

            if not self.go_to_next_page():
                break

            page += 1

        self.driver.quit()

        df = pd.DataFrame(self.products)
        filename = f"amazon_full_scrape_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df.to_csv(filename, index=False)

        print(f"\n✅ Saved {len(self.products)} products to {filename}")


if __name__ == "__main__":
    keyword = input("Enter product keyword to search: ")
    scraper = AmazonFullScraper()
    scraper.scrape_all_pages(keyword, max_pages=5)