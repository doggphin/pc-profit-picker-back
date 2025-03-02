from pcpartpicker import API
import re
import json

# Initialize PCPartPicker API
api = API()

# Get desired part
partType = input("Enter the part type: ").lower()
part_model = input("Enter specific part: ") #Xeon E5-4620

# Fetch CPU data from PCPartPicker API
print("Fetching CPU data from PCPartPicker...")
part_data = api.retrieve(partType)  # Get PartData instance
part_json = part_data.to_json()   # Convert to JSON string
part_dict = json.loads(part_json)  # Convert JSON string to Python dict

# Extract CPU parts from response
parts = part_dict.get(partType, {})

# Function to extract numerical price from price string
def extract_price(price_str):
    """Extract numerical value from price string."""
    if not price_str or "0.00" in str(price_str):
        return None

    match = re.search(r"([\d.]+)", str(price_str))  # Extract digits and decimals
    return float(match.group(1)) if match else float('inf')  # Convert to float or set to high value

# Search for the specific CPU model
matched_part = next((p for p in parts if p.get("model", "").lower() == part_model.lower()), None)

# Display result
if matched_part:
    price = extract_price(matched_part.get("price", ["USD", "0.00"]))
    if price is not None:
        print(f"\nThe price of {matched_part['brand']} {matched_part['model']} is ${price:.2f}")
    else:
        print(f"\nThe price of {matched_part['brand']} {matched_part['model']} is not available.")
else:
    print("\nNo matching part found.")