from time import sleep
from typing import Dict, List
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dataclasses import dataclass
import json

from scrapers.base import Listing, Scraper


@dataclass
class NeweggScraper(Scraper):
    def get_listings(self) -> List[Listing]:
        try:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service)

            with open("credentials.json", "r") as credentials_file:
                credentials : Dict[str, any] = json.load(credentials_file)

            scraper_api_key : str = credentials["scraper_api_key"]

            formatted_item_to_search_for = self.item_to_search_for.replace(" ", "+")

            base_url = f"https://www.newegg.com/p/pl?d={formatted_item_to_search_for}&Order=1"
            # Need to access website through a proxy otherwise newegg blocks us ;(((
            proxied_url = f"http://api.scraperapi.com?api_key={scraper_api_key}&url={base_url}"
            driver.get(proxied_url)

            WebDriverWait(driver, 30).until(
                lambda driver: driver.execute_script('return document.readyState') == 'complete'
            )

            wait = WebDriverWait(driver, 30)

            # Scroll to the bottom to ensure that all content is loaded
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait for listings to show up
            listings = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "item-container")))

            priced_listings : List[Listing] = []
            for listing in listings:
                title = listing.find_element(By.CLASS_NAME, "item-title").text

                price = listing.find_element(By.CLASS_NAME, "price-current").text

                img_element = driver.find_element(By.CSS_SELECTOR, "a.item-img img")
                image_url = img_element.get_attribute("src")

                a_element = driver.find_element(By.CSS_SELECTOR, "item-title")
                product_url = a_element.get_attribute("href")

                priced_listing = Listing(title, price, image_url, product_url)

                priced_listings.append(priced_listing)
        
        except Exception as e:
            print(f"Problem with newegg scraper: {e}")
            return None
        
        if driver is not None:
            driver.close()
        
        print("Priced Listings:")
        print(priced_listings)

        return priced_listings
