import requests
import csv

BASE_URL = "https://dummyjson.com/products"
LIMIT = 30   # how many products per request

headers = {
    "User-Agent": "Mozilla/5.0"
}

def fetch_all_products():
    all_products = []
    skip = 0

    print("Starting full data scrape...\n")

    while True:
        url = f"{BASE_URL}?limit={LIMIT}&skip={skip}"
        print(f"Fetching: {url}")

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print("Failed to fetch data.")
            break

        data = response.json()
        products = data.get("products", [])

        if not products:
            break

        for product in products:
            all_products.append({
                "ID": product.get("id"),
                "Title": product.get("title"),
                "Brand": product.get("brand"),
                "Category": product.get("category"),
                "Price": product.get("price"),
                "Discount %": product.get("discountPercentage"),
                "Rating": product.get("rating"),
                "Stock": product.get("stock"),
                "Description": product.get("description"),
                "Thumbnail": product.get("thumbnail")
            })

        skip += LIMIT

        # Stop when we scraped everything
        if skip >= data.get("total", 0):
            break

    print(f"\nTotal products scraped: {len(all_products)}")
    return all_products


def save_to_csv(data, filename="dummyjson_products.csv"):
    if not data:
        print("No data to save.")
        return

    keys = data[0].keys()

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

    print(f"\nSaved to {filename}")


if __name__ == "__main__":
    products = fetch_all_products()
    save_to_csv(products)