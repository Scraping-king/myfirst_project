| APIData.py | FakeStore API | Title, Price, Category, Rating, Count, Description |
import requests
import csv

API_URL = "https://fakestoreapi.com/products"

headers = {
    "User-Agent": "Mozilla/5.0"
}

def fetch_products():
    print(f"Fetching data from {API_URL}...")
    response = requests.get(API_URL, headers=headers)
    if response.status_code != 200:
        print("Failed to fetch data.")
        return []

    products = response.json()
    result = []
    for product in products:
        result.append({
            "Title": product.get("title"),
            "Price": product.get("price"),
            "Category": product.get("category"),
            "Rating": product.get("rating", {}).get("rate"),
            "Count": product.get("rating", {}).get("count"),
            "Description": product.get("description")
        })
    return result

def save_to_csv(data, filename="fakestore_products.csv"):
    if not data:
        print("No data to save.")
        return
    keys = data[0].keys()
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)
    print(f"\nSaved {len(data)} products to {filename}")

if __name__ == "__main__":
    products = fetch_products()
    save_to_csv(products)
