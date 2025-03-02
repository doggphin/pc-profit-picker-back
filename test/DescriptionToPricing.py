from openai import OpenAI
import re
import ast
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the API key
api_key_env = os.getenv("OPENAI_API_KEY")

question = "Extract the PC components from the following description and return a Python dictionary. The dictionary keys must be 'cpu', 'video-card', 'memory', 'storage', 'powersupply', 'motherboard', and 'case'. Match each component to a real part name from PC Part Picker. If a component is missing from the description, set its value to None. The response must be only a valid Python dictionary—no explanations, text, or formatting outside the dictionary itself."
description = "ABS Cyclone Aqua Gaming PC - Windows 11 Home - Intel Core i5-14400F - GeForce RTX 4060 - DLSS 3 - AI-Powered Performance - 32GB DDR5 6000 - 1TB M.2 NVMe SSD - CA14400F40603"
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

pc_components = ast.literal_eval(listing_components)

print(pc_components)