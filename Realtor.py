from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Correct way
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

base_url = 'https://www.realtor.com/realestateandhomes-search/New-York/pg-{}'

all_data = []

for page in range(1, 6):
    print(f'Scraping Page {page}...')
    driver.get(base_url.format(page))
    time.sleep(5)

    listings = driver.find_elements(By.CSS_SELECTOR, 'li[data-testid="result-card"]')

    for item in listings:
        try:
            title = item.find_element(By.CSS_SELECTOR, 'div[data-label="pc-address"]').text
        except:
            title = 'N/A'
        try:
            price = item.find_element(By.CSS_SELECTOR, 'span[data-label="pc-price"]').text
        except:
            price = 'N/A'
        try:
            beds = item.find_element(By.CSS_SELECTOR, 'li[data-label="pc-meta-beds"]').text
        except:
            beds = 'N/A'
        try:
            baths = item.find_element(By.CSS_SELECTOR, 'li[data-label="pc-meta-baths"]').text
        except:
            baths = 'N/A'
        try:
            sqft = item.find_element(By.CSS_SELECTOR, 'li[data-label="pc-meta-sqft"]').text
        except:
            sqft = 'N/A'

        all_data.append([title, price, beds, baths, sqft])

    time.sleep(2)

driver.quit()

df = pd.DataFrame(all_data, columns=['Title', 'Price', 'Beds', 'Baths', 'Sqft'])
df.to_csv('realtor_ny_listings.csv', index=False, encoding='utf-8')

print("Scraping Completed Successfully!")
