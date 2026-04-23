# DAY 6: Web Scraping Machine Learning Datasets

import requests
from bs4 import BeautifulSoup

print("===================================")
print("DAY 6 - WEB SCRAPING ML DATASETS")
print("===================================")

# URL of UCI ML Repository
url = "https://archive.ics.uci.edu/"

print("\nConnecting to website...")

# Send request
response = requests.get(url)

# Check if request succeeded
if response.status_code == 200:
    print("Connection successful!")
else:
    print("Failed to connect")
    exit()

# Parse the HTML
soup = BeautifulSoup(response.text, "html.parser")

print("\nPage Title:")
print(soup.title.text)

print("\nExtracting links from the page...\n")

# Find all links
links = soup.find_all("a")

# Print first 20 links
count = 0
for link in links:
    
    text = link.text.strip()
    href = link.get("href")

    if text != "" and href != None:
        print(f"Name: {text}")
        print(f"Link: {href}")
        print("----------------------------")

        count += 1

    if count == 20:
        break

print("\nScraping completed!")