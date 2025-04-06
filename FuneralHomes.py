import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# Set up Chrome options to disable SSL verification
chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--headless')  # Run headless, optional

# Set up ChromeDriver with webdriver_manager (automatically manages the driver path)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Open the website
driver.get("https://www.dignitymemorial.com/funeral-homes")

# Allow time for dynamic content to load
time.sleep(5)

# Scrape the funeral home data using updated syntax
funeral_homes = driver.find_elements(By.CLASS_NAME, 'item-details')

# Open a CSV file to write the data
with open('funeral_homes.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Name', 'Address', 'Phone']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    # Write the header row
    writer.writeheader()

    # Loop through the funeral homes and write each one to the CSV file
    for home in funeral_homes:
        try:
            name = home.find_element(By.CLASS_NAME, 'business-name').text
            address = home.find_element(By.CLASS_NAME, 'address').text
            phone = home.find_element(By.CLASS_NAME, 'phone').text
            writer.writerow({'Name': name, 'Address': address, 'Phone': phone})
        except Exception as e:
            print("Error scraping a funeral home:", e)

# Quit the browser
driver.quit()

print("Data saved to funeral_homes.csv")
