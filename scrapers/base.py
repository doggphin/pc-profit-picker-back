import abc
from dataclasses import dataclass
from abc import ABC
from typing import List

from dotenv import load_dotenv
import os

load_dotenv()
SCRAPER_API_KEY : str = os.getenv("SCRAPER_API_KEY")

@dataclass
class Listing:
    title : str
    price : str
    image_url : str
    product_url : str


@dataclass
class Scraper(ABC):
    item_to_search_for : str
    limit : int = None
    
    @abc.abstractmethod
    def get_listings(self) -> List[Listing]:
        pass