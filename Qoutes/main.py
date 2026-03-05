from scraper.quotes_scraper import scrape_quotes, save_to_csv


def main():
    print("=== Quotes To Scrape - Web Scraper ===\n")

    quotes = scrape_quotes()

    if quotes:
        save_to_csv(quotes, filename="data/quotes.csv")
        print("\nScraping completed successfully!")
    else:
        print("\nNo quotes were scraped.")


if __name__ == "__main__":
    main()