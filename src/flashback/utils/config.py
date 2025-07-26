import os
from dotenv import load_dotenv


def load_config() -> dict:
    load_dotenv()
    
    youtube_api_key = os.getenv('YOUTUBE_API_KEY')
    
    if not youtube_api_key:
        raise ValueError(
            "YOUTUBE_API_KEY environment variable is required. "
            "Please set it in your .env file or environment."
        )
    
    return {
        'youtube_api_key': youtube_api_key,
    } 