import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import argparse
import sys
parser = argparse.ArgumentParser(description="Scrape product reviews")

parser.add_argument("--company", required=True, help="Company name")
parser.add_argument("--start", required=True, help="Start date YYYY-MM-DD")
parser.add_argument("--end", required=True, help="End date YYYY-MM-DD")
parser.add_argument("--source", required=True, help="g2 or capterra")

args = parser.parse_args()
try:
    start_date = datetime.strptime(args.start, "%Y-%m-%d")
    end_date = datetime.strptime(args.end, "%Y-%m-%d")
except ValueError:
    print("❌ Date format should be YYYY-MM-DD")
    sys.exit()
source = args.source.lower()
company = args.company.lower()

if source == "g2":
    url = f"https://www.g2.com/products/{company}/reviews"
elif source == "capterra":
    url = f"https://www.capterra.com/p/{company}/reviews/"
else:
    print("❌ Source must be g2 or capterra")
    sys.exit()
headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

if response.status_code != 200:
    print("⚠️ Live scraping blocked by website. Using sample data.")

    reviews = [
        {
            "title": "Great Product",
            "review": "Very helpful and easy to use",
            "date": "2024-05-10",
            "source": source,
            "company": args.company
        },
        {
            "title": "Good Customer Support",
            "review": "Support team responds quickly",
            "date": "2024-06-01",
            "source": source,
            "company": args.company
        }
    ]

    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(reviews, f, indent=4)

    print("✅ Sample reviews saved to output.json")
    sys.exit()
soup = BeautifulSoup(response.text, "html.parser")
review_blocks = soup.find_all("div")
reviews = []

for block in review_blocks:
    title_tag = block.find("h3")
    desc_tag = block.find("p")
    date_tag = block.find("span")

    if not title_tag or not desc_tag or not date_tag:
        continue

    title = title_tag.text.strip()
    description = desc_tag.text.strip()
    date_text = date_tag.text.strip()

    try:
        review_date = datetime.strptime(date_text, "%Y-%m-%d")
    except:
        continue

    if start_date <= review_date <= end_date:
        reviews.append({
            "title": title,
            "review": description,
            "date": date_text,
            "source": source,
            "company": args.company
        })
with open("output.json", "w", encoding="utf-8") as f:
    json.dump(reviews, f, indent=4)

print(f"✅ {len(reviews)} reviews saved to output.json")