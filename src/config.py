import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GITLAB_URL = os.getenv("GITLAB_URL", "https://gitlab.com")
    GITLAB_TOKEN = os.getenv("GITLAB_TOKEN")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    

    GEMINI_MODEL_NAME = "gemini-2.0-flash" 

    if not GITLAB_TOKEN or not GEMINI_API_KEY:
        raise ValueError("Please set GITLAB_TOKEN and GEMINI_API_KEY in .env file")