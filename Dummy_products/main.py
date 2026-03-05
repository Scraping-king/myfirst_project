from Scraper.product_scraper import fetch_all_products, save_to_csv


def main():
    print("=== DummyJSON Product Scraper ===\n")

    products = fetch_all_products()

    if products:
        save_to_csv(products)
        print("\nScraping completed successfully!")
    else:
        print("\nNo products found.")


if __name__ == "__main__":
    main()