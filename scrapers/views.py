from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from scrapers.newegg.scraper import NeweggScraper


@api_view(["GET"])
def flips(request):
    return Response({
        "listings" : [
            {
                "image_url" : "https://avatars.githubusercontent.com/u/38893970?s=64&v=4",
                "title" : "ABS Cyclone Aqua Gaming PC - Windows 11 Home - Intel Core i7-14700F - RTX 4060Ti 8GB - DLSS 3.5 - AI-Powered Performance - 32GB DDR5 6000MHz - 1TB M.2 NVMe SSD - CA14700F4060TI3",
                "product_url" : "http://google.com",
                "price" : 50000,
                "profit" : 4599
            },
            {
                "image_url" : "https://i.ytimg.com/an_webp/sSOxPJD-VNo/mqdefault_6s.webp?du=3000&sqp=CIzcjb4G&rs=AOn4CLCvbQA6gCcuLeOkKf0wQ6eyEwe4tA",
                "title" : "USED - VERY GOOD IPASON Gaming PC Desktop Intel i5 12400F(up to 4.4GHz) , RTX 4060, 1TB NVME SSD, 16GB DDR4 RAM , ATX case , Windows 11 Home 64-bit",
                "product_url" : "http://zombo.com",
                "price" : 60000,
                "profit" : 5599
            },
        ]
    })


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