| w3school.py | W3Schools | Tag, Description |
import requests
from bs4 import BeautifulSoup
import csv

def scrape_w3schools_html_tags():
    url = "https://www.w3schools.com/tags/default.asp"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    results = []
    table = soup.find("table", {"class": "ws-table-all"})
    
    if not table:
        print("❌ Could not find the tags table.")
        return

    rows = table.find_all("tr")[1:]  # Skip header

    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 2:
            tag = cols[0].text.strip()
            description = cols[1].text.strip()
            results.append({"Tag": tag, "Description": description})

    return results

def save_to_csv(data, filename="w3schools_html_tags.csv"):
    if not data:
        print("No data to save.")
        return
    keys = data[0].keys()
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)
    print(f"✅ Saved {len(data)} rows to {filename}")

if __name__ == "__main__":
    data = scrape_w3schools_html_tags()
    save_to_csv(data)
