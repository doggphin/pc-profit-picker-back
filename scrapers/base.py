import abc
from dataclasses import dataclass
from abc import ABC
from typing import List


@dataclass
class Listing:
    title : str
    price : str
    image_url : str
    product_url : str


@dataclass
class Scraper(ABC):
    item_to_search_for : str
    
    @abc.abstractmethod
    def get_listings(self) -> List[Listing]:
        pass