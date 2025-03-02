import re
import time
from typing import List
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dataclasses import dataclass
import urllib.parse

from scrapers.base import Listing, Scraper, SCRAPER_API_KEY

TIME_TO_WAIT_BETWEEN_REQUESTS = 30
@dataclass
class EbayScraper(Scraper):
    def get_listings(self) -> List[Listing]:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)

        listing : List[Listing] = []

        try:
            formatted_search = self.item_to_search_for.replace(" ", "+")
            formatted_search = urllib.parse.quote(formatted_search)

            url = f"https://www.ebay.com/sch/i.html?_nkw={formatted_search}&_sacat=0&_from=R40&LH_BIN=1&_sop=15"

            # Add proxy
            # url = f"http://api.scraperapi.com?api_key={SCRAPER_API_KEY}&url={url}"
            
            driver.get(url)

            WebDriverWait(driver, 10).until(
                lambda driver: driver.execute_script('return document.readyState') == 'complete'
            )

            wait = WebDriverWait(driver, 10)

            # Scroll to the bottom to ensure that all content is loaded
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait for listings to show up
            listings_river = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.srp-river-results")))
            first_listing = listings_river.find_element(By.CSS_SELECTOR, "div.s-item__wrapper")

            if first_listing == None:
                return []

            # Get the image
            time.sleep(TIME_TO_WAIT_BETWEEN_REQUESTS)
            img_url = first_listing.find_elements("xpath", '//img[starts-with(@src, "https://i.ebayimg")]')[0].get_attribute("src")

            # Get the title of the listing, which is located inside a <span role="heading"> with a span inside and some plaintext after
            # We're interested in the plaintext after
            title_element_inner_html = first_listing.find_element(By.CSS_SELECTOR, "div.s-item__title").get_attribute("innerHTML")
            match = re.search(r"-->([^<]+)<", title_element_inner_html)
            title = match[1].strip()
            #full_text = heading_element.text
            #print(f"full text is {full_text}")
            #title = full_text.split("\n")[-1].strip()

            # Get base price; convert "$662.90" to 662.90
            base_price_element_inner_html = first_listing.find_element(By.CSS_SELECTOR, "span.s-item__price").get_attribute("innerHTML")
            match = re.search(r"\$([\d,.]+)", base_price_element_inner_html)
            base_price = float(match.group(1))
            #base_price_text = base_price_element.text
            #base_price = base_price_text.replace("$", "").strip()

            # base_price_text : str = first_listing.find_element(By.CSS_SELECTOR, "s-item__price").txt
            # base_price = float(base_price_text[1:])
            #print(base_price)

            shipping_price : float = 0

            try:
                shipping_price_element : str = first_listing.find_element(By.CSS_SELECTOR, "span.s-item__shipping.s-item__logisticsCost")
                # Get shipping price; convert "+$52.80 delivery" to 52.80 or "Free Delivery" to 0
                shipping_price_element_inner_html = shipping_price_element.get_attribute("innerHTML")
                is_free_delivery : bool = "Free delivery" in shipping_price_element_inner_html
                if not is_free_delivery:
                    match = re.search(r"\+([\d,.]+)", shipping_price_element_inner_html)
                    shipping_price : float = float(match.group(1))
            # There's variants of this I don't feel like handling. If logisticsCost doesnt exist, just use 0 shipping cost
            except Exception as e:
                pass

            # Get total price as base + shipping price
            total_price : float = base_price + shipping_price

            listing = [Listing(title, total_price, img_url, "www.google.com")]
            print(listing)

        except Exception as e:
            print(e)

        return listing

        