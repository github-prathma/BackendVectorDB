## to test if .env file is loaded correctly
from dotenv import load_dotenv
import os

load_dotenv()
print("COHERE_API_KEY from .env:", os.getenv("COHERE_API_KEY"), flush=True)
