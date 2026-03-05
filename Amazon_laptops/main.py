from scraper.tracker import SeleniumPriceTracker


def main():
    print("=" * 50)
    print("🛒 Amazon Price Tracker (Selenium)")
    print("=" * 50)

    tracker = SeleniumPriceTracker()

    # You can modify these products
    products = [
        ("Apple AirPods Pro", "https://www.amazon.com/dp/B0BDHWDR12"),
        ("Echo Dot 5th Gen", "https://www.amazon.com/dp/B09B8V1LZ3"),
    ]

    for name, url in products:
        tracker.add_product(name, url)

    print(f"\n📊 Tracking {len(products)} products...\n")

    tracker.track_prices()

    print("\n✅ Price tracking completed successfully!")


if __name__ == "__main__":
    main()