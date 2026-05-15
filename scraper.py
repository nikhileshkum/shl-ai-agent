import requests
from bs4 import BeautifulSoup
import json

BASE_URL = "https://www.shl.com/solutions/products/product-catalog/"

response = requests.get(BASE_URL)
soup = BeautifulSoup(response.text, "html.parser")

assessments = []

cards = soup.find_all("a")

for card in cards:
    title = card.get_text(strip=True)
    href = card.get("href")

    if title and href and "/products/" in href:
        assessments.append({
            "name": title,
            "url": href if href.startswith("http") else f"https://www.shl.com{href}",
            "description": "",
            "test_type": ""
        })

# Remove duplicates
unique = {item["url"]: item for item in assessments}

with open("catalog.json", "w") as f:
    json.dump(list(unique.values()), f, indent=2)

print(f"Saved {len(unique)} assessments")