from scraper.amazon_scraper import AmazonSearchScraper
from datetime import datetime
import os


def main():
    print("=" * 50)
    print("🛒 Amazon Search Results Scraper (Playwright)")
    print("=" * 50)

    keyword = input("Enter product keyword to search: ").strip()

    if not keyword:
        print("❌ Keyword cannot be empty.")
        return

    scraper = AmazonSearchScraper(keyword)

    print(f"\n🔍 Starting scrape for: {keyword}")
    print("Please wait...\n")

    scraper.run()

    print("\n✅ Scraping completed successfully!")
    print(f"📁 Check the generated CSV file in project folder.")


if __name__ == "__main__":
    main()