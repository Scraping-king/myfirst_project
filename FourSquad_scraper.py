from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Optional: No browser pop-up
options.add_argument('--disable-gpu')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

url = "https://foursquare.com/v/new-york-ny/4bf58dd8d48988d1c4941735"
driver.get(url)
time.sleep(5)  # Wait for JS to load

data = []

# Scroll to load more results
for _ in range(3):  
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

listings = driver.find_elements(By.CLASS_NAME, 'venueDetailsContainer__venueTitle___1fd0g')  # Might change → Inspect site

for listing in listings:
    try:
        name = listing.text
        data.append({
            'Name': name,
        })
    except:
        pass

driver.quit()

df = pd.DataFrame(data)
df.to_csv('foursquare_ny.csv', index=False)

print("Scraping Completed!")
