from pcpartpicker import API
import re
import json

# Initialize PCPartPicker API
api = API()

def extract_price(price_str):
    """Extract numerical value from price string."""
    if not price_str or "0.00" in str(price_str):
        return None
    match = re.search(r"([\d.]+)", str(price_str))  # Extract digits and decimals
    return float(match.group(1)) if match else None

# Get prebuilt PC price
PrebuildPrice = float(input("Enter the price of the prebuilt PC: "))

# Define parts dictionary
parts = {
    'cpu': 'Xeon E5-4620',
    'video-card': 'GeForce RTX 3080',
    'memory': 'T-FORCE DARK Z 32 GB',
    'internal-hard-drive': 'UltimaPro X2',
    'power-supply': 'Pure Power 9',
    'motherboard': 'X370 GAMING PRO',
    'case': 'Playa Slim'
}

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
    print("\nProfit to be made of: ${:.2f}".format(price_of_components - PrebuildPrice))
elif price_of_components < PrebuildPrice:
    print("\n No profit to be made.")
else:
    print("\n Cost price is equal to the prebuilt price.")