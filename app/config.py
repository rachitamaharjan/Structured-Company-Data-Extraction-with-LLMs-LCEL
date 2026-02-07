import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI configuration 
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Gemini configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

DB_URL = os.getenv("DB_URL")
