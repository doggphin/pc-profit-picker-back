from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from scrapers.newegg.scraper import NeweggScraper
from scrapers.base import Listing

from openai import OpenAI
import re
import ast
import os
import json
from dotenv import load_dotenv
from pcpartpicker import API

@api_view(["GET"])
def flips(request, budget : int):

    # Get listings
    newegg_scraper = NeweggScraper(item_to_search_for="prebuilt 3060")
    listings = newegg_scraper.get_listings()

    # Iterate through listings
    listing = listings[0]
    description = listing.title
    PrebuildPrice = listing.price

    # Load environment variables from .env file
    load_dotenv()

    # Access the API key
    api_key_env = os.getenv("OPENAI_API_KEY")

    # Extract pc components into readable format
    question = "Extract the PC components from the following description and return a Python dictionary. The dictionary keys must be 'cpu', 'video-card', 'memory', 'storage', 'powersupply', 'motherboard', and 'case'. Match each component to a real part name from PC Part Picker. If a component is missing from the description, set its value to None. The response must be only a valid Python dictionary—no explanations, text, or formatting outside the dictionary itself."
    prompt = f"{question}\n{description}"

    client = OpenAI(
        api_key=api_key_env
    )
    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    store=True,
    messages=[
        {"role": "user", "content": prompt}
    ]
    )

    message = completion.choices[0].message
    content = message.content
    listing_components = re.sub(r'```(python)?\n', '', content).strip("```")

    parts = ast.literal_eval(listing_components)

    # Initialize PCPartPicker API
    api = API()

    def extract_price(price_str):
        """Extract numerical value from price string."""
        if not price_str or "0.00" in str(price_str):
            return None
        match = re.search(r"([\d.]+)", str(price_str))  # Extract digits and decimals
        return float(match.group(1)) if match else None

    price_of_components = 0
    found_parts = {}

    for partType, part_model in parts.items():
        if part_model:
            print(f"Fetching {partType} data from PCPartPicker...")
            part_data = api.retrieve(partType)  # Fetch data
            part_json = part_data.to_json()
            part_dict = json.loads(part_json)
            available_parts = part_dict.get(partType, [])
            
            if partType == "video-card":
                matched_part = next((p for p in available_parts if p.get("chipset", "").lower() == part_model.lower()), None)
            else:
                matched_part = next((p for p in available_parts if p.get("model", "").lower() == part_model.lower()), None)
            
            if matched_part:
                price = extract_price(matched_part.get("price", ["USD", "0.00"]))
                if price is not None:
                    price_of_components += price
                    found_parts[partType] = price
                    print(f"{matched_part['brand']} {matched_part['model']} - ${price:.2f}")
                else:
                    print(f"Price not available for {matched_part['brand']} {matched_part['model']}.")
            else:
                print(f"No matching part found for {part_model}.")

    # Display the total price of the custom build
    print(f"\nTotal Price of Components: ${price_of_components:.2f}")
    print(f"Prebuilt PC Price: ${PrebuildPrice:.2f}")

    # Compare prices
    if price_of_components > PrebuildPrice:
        return "\nProfit to be made of: ${:.2f}".format(price_of_components - PrebuildPrice)
    elif price_of_components < PrebuildPrice:
        return "\n No profit to be made."
    else:
        return "\n Cost price is equal to the prebuilt price."

@api_view(["GET"])
def test(request):
    scraper = NeweggScraper(item_to_search_for="4060 TI 16GB")
    listings = scraper.get_listings()
    
    for listing in listings:
        print(listing.title)
        print(listing.image_url)
        print(listing.price)
        print(listing.product_url)
        print("=====")
    
    return Response()