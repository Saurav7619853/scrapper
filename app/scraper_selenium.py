from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os
import time
import requests
from app.db import CacheDB
from app.storage_strategy import StorageStrategy
from app.storage_strategies.json_storage import JsonStorageStrategy
from app.notification_strategy import NotificationStrategy
from app.notification_strategies.console_notification import ConsoleNotification
import re
from dotenv import load_dotenv
load_dotenv()

class Scraper:
    def __init__(self, page_limit=None, proxy=None, storage_strategy: StorageStrategy = JsonStorageStrategy(), notification_strategy: NotificationStrategy = ConsoleNotification()):
        self.base_url = os.getenv('URL')
        self.page_limit = page_limit or 3
        self.proxy = proxy
        self.cache = CacheDB()
        self.data = []
        self.storage_strategy = storage_strategy
        self.notification_strategy = notification_strategy
        self.driver = self.setup_driver()
        self.max_retries = int(os.getenv('MAX_RETRIES', 3))

    def setup_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        
        if self.proxy:
            chrome_options.add_argument(f'--proxy-server={self.proxy}')
        
        driver = webdriver.Chrome(options=chrome_options)
        return driver

    def scrape_page(self, page_number):
        retry_count = 0
        page_url = f"{self.base_url}{page_number}/"
        
        while retry_count < self.max_retries:
            try:
                self.driver.get(page_url)
                time.sleep(2)
                return self.driver
            except Exception as e:
                retry_count += 1
                print(f"Failed to fetch page {page_number}: {e}, retrying... ({retry_count}/{self.max_retries})")
                time.sleep(2)
                
        print(f"Failed to fetch page {page_number} after {self.max_retries} retries.")
        return None

    def scrape_products(self):
        for page in range(1, self.page_limit + 1):
            driver = self.scrape_page(page)
            if not driver:
                print(f"Skipping page {page} after multiple failed attempts.")
                continue

            products = driver.find_elements(By.CSS_SELECTOR, 'ul.products.columns-4 li.product')
            product_links = []
        
            # first extract product links from the page
            for product in products:
                product_link_element = product.find_element(By.CSS_SELECTOR, 'div.mf-product-thumbnail a')
                product_link = product_link_element.get_attribute('href')
                product_links.append(product_link)

            # visit each product link separately
            for product_link in product_links:
                driver.get(product_link)
                time.sleep(1)
                name = self.extract_product_name()
                price = self.extract_product_price()
                img_url = self.extract_product_image_url()
                if not self.cache.is_updated(name, price):
                    image_path = self.download_image(img_url)
                    self.data.append({
                        "product_title": name,
                        "product_price": price,
                        "path_to_image": image_path
                    })
                    self.cache.update_cache(name, price)
                
                # return to the original product page
                driver.get(f"{self.base_url}/page/{page}")
                time.sleep(1)
        self.save_data()
        self.notify_scrape_status()
        return self.data

    def extract_product_name(self):
        try:
            name_element = self.driver.find_element(By.CSS_SELECTOR, 'h1.product_title.entry-title')
            return name_element.text.strip()
        except Exception as e:
            print(f"Error product name: {e}")
            return None

    def extract_product_price(self):
        try:
            price_element = self.driver.find_element(By.CSS_SELECTOR, 'p.price .woocommerce-Price-amount')
            price_numeric = re.sub(r'[^\d.]', '', price_element.text.strip())
            return price_numeric
        except Exception as e:
            print(f"Error product price: {e}")
            return None

    def extract_product_image_url(self):
        try:
            img_element = self.driver.find_element(By.CSS_SELECTOR, 'div.woocommerce-product-gallery__image img')
            return img_element.get_attribute('src')
        except Exception as e:
            print(f"Error product image: {e}")
            return None

    def download_image(self, img_url):
        img_data = requests.get(img_url).content
        img_name = img_url.split("/")[-1]
        img_path = os.path.join("images", img_name)
        if not os.path.exists('images'):
            os.makedirs('images')
        with open(img_path, 'wb') as img_file:
            img_file.write(img_data)
        return img_path

    def save_data(self):
        self.storage_strategy.save(self.data)

    def notify_scrape_status(self):
        message = f"Scraped {len(self.data)} products in the current session."
        self.notification_strategy.notify(message)

    def close(self):
        self.driver.quit()
