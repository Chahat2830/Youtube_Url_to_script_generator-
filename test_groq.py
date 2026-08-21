import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq


# Find project root
BASE_DIR = Path(__file__).resolve().parent

# Load .env
load_dotenv(BASE_DIR / ".env")

# Get API key
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found")


# Create client
client = Groq(api_key=api_key)


# Get available models
models = client.models.list()

print("\nAvailable Groq models:\n")

for model in models.data:
    print(model.id)