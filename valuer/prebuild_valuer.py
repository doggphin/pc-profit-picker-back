import ast
import asyncio
from dataclasses import dataclass
import json
import os
import re
from typing import Dict
from dotenv import load_dotenv
from openai import OpenAI

from scrapers.base import Listing
from scrapers.ebay.scraper import EbayScraper

load_dotenv()
OPENAI_API_KEY : str = os.getenv("OPENAI_API_KEY")

@dataclass
class PrebuildDeconstructor():
    listing_title : str
    listing_price : int

    def get_value(self) -> Dict[str, Listing]:
        """
        Returns the name of each component in the pre-built PC and how much they're worth on ebay, and its listing.
        """

        # First, ask OpenAI to deconstruct the name of the PC into PC parts.
        openai_api_client = OpenAI(api_key = OPENAI_API_KEY)
        completion = openai_api_client.chat.completions.create(
            model = "gpt-4o-mini",
            store = True,
            messages = [
                {"role": "user", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Convert '{self.listing_title}' into structured JSON, where the values are strings." }
            ],
            functions=[
                {
                    "name": "convert_to_json",
                    "description": "Converts given text into a structured JSON format.",
                    "parameters" : {
                        "type" : "object",
                        "properties": {
                            "cpu": { "type" : "string" },
                            "video-card": { "type" : "string" },
                            "memory": { "type" : "string" },
                            "storage": { "type" : "string" },
                            "powersupply": { "type" : "string" },
                            "motherboard": { "type" : "string" },
                            "case": { "type" : "string" },
                        },
                        "required": ["title", "description", "category", "date"]
                    }
                }
            ],
            function_call={ "name": "convert_to_json" }
        )
        choice = completion.choices[0]
        components : Dict[str, str] = json.loads(choice.message.function_call.arguments)

        # Next, take each of those parts and look up how much they're going for on ebay.
        component_resale_listings : Dict[str, Listing] = {}
        for component_type, component_name in components.items():
            if component_name == None or component_name.strip() == "":
                continue

            ebay_scraper = EbayScraper(component_name, 1)
            listings = ebay_scraper.get_listings()

            component_resale_listings[component_type] = listings[0]
        
        # Return the dictionary of part names to their listings on ebay.
        return component_resale_listings