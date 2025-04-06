import bs4
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

base_url = "https://www.yelp.com/search?find_desc=Optometrists&find_loc=New+York%2C+NY&start={}"

data = []

for page in range(0, 50, 10):  # Scrape 5 pages
    url = base_url.format(page)
    print(f"Scraping: {url}")
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    listings = soup.find_all('div', {'class': 'container__09f24__21w3G'})  # Updated correct class

    for item in listings:
        name_tag = item.find('a', {'class': 'css-19v1rkv'})  # Business Name
        address_tag = item.find('address')  # Address
        phone_tag = item.find('p', {'class': 'css-8jxw1i'})  # Phone

        name = name_tag.text if name_tag else None
        address = address_tag.text if address_tag else None
        phone = phone_tag.text if phone_tag else None

        if name:  # Only add if business name exists
            data.append({
                'Name': name,
                'Address': address,
                'Phone': phone
            })

    time.sleep(2)

df = pd.DataFrame(data)
df.to_csv('yelp_optometrists_ny.csv', index=False)

print("Scraping completed. Data saved to yelp_optometrists_ny.csv")
