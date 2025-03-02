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

from scrapers.listing import Listing, Scraper


@dataclass
class NeweggScraper(Scraper):
    def get_listings(self) -> List[Listing]:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)

        with open("credentials.json", "r") as credentials_file:
            credentials : Dict[str, any] = json.load(credentials_file)

        scraper_api_key : str = credentials["scraper_api_key"]

        formatted_item_to_search_for = self.search_for.replace(" ", "+")

        base_url = f"https://www.newegg.com/p/pl?d={formatted_item_to_search_for}&Order=1"
        # Need to access website through a proxy otherwise newegg blocks us ;(((
        proxied_url = f"http://api.scraperapi.com?api_key={scraper_api_key}&url={base_url}"
        driver.get(proxied_url)

        WebDriverWait(driver, 10).until(
            lambda driver: driver.execute_script('return document.readyState') == 'complete'
        )

        wait = WebDriverWait(driver, 10)

        # Scroll to the bottom to ensure that all content is loaded
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait for listings to show up
        listings = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "item-container")))

        priced_listings : List[Listing] = []
        for listing in listings:
            title = listing.find_element(By.CLASS_NAME, "item-title").text
            price = listing.find_element(By.CLASS_NAME, "price-current").text
            priced_listing = Listing(title, price)
            priced_listings.append(priced_listing)
