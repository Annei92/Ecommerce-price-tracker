# scrapers/books.py

import requests
from bs4 import BeautifulSoup
from datetime import datetime

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
    )
}

def scrape_book_product(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code != 200:
            print("❌ Failed to fetch page:", response.status_code)
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.h1.get_text(strip=True)
        price = soup.select_one(".price_color").get_text(strip=True)
        availability = soup.select_one(".availability").get_text(strip=True)
        rating_tag = soup.select_one(".star-rating")

        rating = "Unknown"
        if rating_tag and "class" in rating_tag.attrs:
            for cls in rating_tag["class"]:
                if cls in ["One", "Two", "Three", "Four", "Five"]:
                    rating = cls
                    break

        return {
            "timestamp": datetime.now().isoformat(),
            "site": "BooksToScrape",
            "product_name": title,
            "price": price,
            "rating": rating,
            "availability": availability,
            "url": url
        }

    except Exception as e:
        print(f"❌ Error during scraping: {e}")
        return None
