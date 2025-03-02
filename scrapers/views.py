from ast import List
from typing import Dict
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from scrapers.newegg.scraper import NeweggScraper
from scrapers.base import Listing

from valuer.prebuild_valuer import PrebuildDeconstructor


@api_view(["GET"])
def flips(request):

    # Get listings
    newegg_scraper = NeweggScraper(item_to_search_for="prebuilt 3060")
    listings = newegg_scraper.get_listings()

    prebuilt_listing = listings[0]
    listing_title = prebuilt_listing.title
    listing_price = prebuilt_listing.price

    prebuild_valuer = PrebuildDeconstructor(listing_title, listing_price)
    prebuild_components = prebuild_valuer.get_value()

    total_value : float = 0
    for component in prebuild_components.values():
        total_value += component.price

    prebuilt_json = prebuilt_listing.to_dict()
    prebuilt_json["profit"] = total_value - float(prebuilt_listing.price)
    print("Profit: ", total_value - float(prebuilt_listing.price))

    result = prebuilt_json
    result["components"] = {}

    for component_type, component in prebuild_components.items():
        result["components"][component_type] = component.to_dict()


    return Response(result)

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


@api_view(["GET"])
def test_flips(request):
    return Response({
  "title": "AOACE Gaming PC Desktop INTEL Core i5 12400F 2.5 GHz, NVIDIA RTX 4060 8G DLSS 3, 32GB DDR4 RAM 3200MHz,1TB NVMe PCIe4.0, Wi-Fi6E, Game Design Office console,Sea View Room,Windows 11 Home 64-bit",
  "price": "779.99 ",
  "image_url": "https://c1.neweggimages.com/productimage/nb300/BV1MS2406280ILHWI06.jpg",
  "product_url": "unfinished",
  "profit": -171.73000000000002,
  "components": {
    "cpu": {
      "title": "CN-0WTY0Y For Dell Laptop Inspiron 17R 3721 5721 with i7-3517U HM76 Motherboard",
      "price": 77,
      "image_url": "https://i.ebayimg.com/images/g/9HUAAOSw8M5nPAMM/s-l500.webp",
      "product_url": "www.google.com"
    },
    "video-card": {
      "title": "4711377115469 MSI GeForce RTX 4060 GAMING 8G DLSS 3 Grafikkarte MSI",
      "price": 494.28,
      "image_url": "https://i.ebayimg.com/images/g/D8cAAOSwmAhm0WvN/s-l500.webp",
      "product_url": "www.google.com"
    },
    "memory": {
      "title": "Patriot SL 8GB 16GB 32GB DDR4 RAM 3200MHz PC4-25600 SODIMM 260-Pin Laptop Memory",
      "price": 16.99,
      "image_url": "https://i.ebayimg.com/images/g/rF8AAOSwWZFnLU-F/s-l500.webp",
      "product_url": "www.google.com"
    },
    "storage": {
      "title": "Micron 2450 256GB SSD M.2 2230 NVMe PCIe Gen4x4 MTFDKBK256TFK",
      "price": 19.99,
      "image_url": "https://i.ebayimg.com/images/g/cTcAAOSw3WxnpYLB/s-l500.webp",
      "product_url": "www.google.com"
    }
  }
})