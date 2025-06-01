import os
import pandas as pd
from scrapers.books import scrape_book_product

CSV_FILE = "data/price_log.csv"

def init_csv(file_path):
    if not os.path.exists(file_path):
        columns = ["timestamp", "site", "product_name", "price", "rating", "availability", "url"]
        df = pd.DataFrame(columns=columns)
        df.to_csv(file_path, index=False)
        print("✅ Initialized CSV.")

def save_to_csv(data, file_path):
    df = pd.DataFrame([data])
    df.to_csv(file_path, mode="a", index=False, header=not os.path.exists(file_path))
    print("✅ Data saved.")

if __name__ == "__main__":
    init_csv(CSV_FILE)

    url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    print(f"🔍 Scraping: {url}")
    product_data = scrape_book_product(url)

    if product_data:
        save_to_csv(product_data, CSV_FILE)
        print("✅ Scraped:", product_data)
    else:
        print("❌ Failed to extract product data.")

