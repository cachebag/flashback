import os
import json
import getpass
from pathlib import Path
from typing import Dict, Optional
from dotenv import load_dotenv
from platformdirs import user_config_dir


def _get_config_dir() -> Path:
    config_dir = Path(user_config_dir("ytflashback", "ytflashback"))
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir


def _get_config_file() -> Path:
    return _get_config_dir() / "config.json"


def load_config() -> dict:
    load_dotenv()
    youtube_api_key = os.getenv('YOUTUBE_API_KEY')
    
    config_file = _get_config_file()
    config_data = {}
    
    if config_file.exists():
        try:
            with open(config_file, 'r') as f:
                config_data = json.load(f)
        except (json.JSONDecodeError, IOError):
            config_data = {}
    
    if not youtube_api_key:
        youtube_api_key = config_data.get('youtube_api_key')
    
    theme_preference = config_data.get('theme_preference', 'textual-dark')
    
    return {
        'youtube_api_key': youtube_api_key,
        'theme_preference': theme_preference,
        'has_api_key': youtube_api_key is not None,
    }


def save_config(config: Dict) -> None:
    config_file = _get_config_file()
    
    existing_config = {}
    if config_file.exists():
        try:
            with open(config_file, 'r') as f:
                existing_config = json.load(f)
        except (json.JSONDecodeError, IOError):
            existing_config = {}
    
    existing_config.update(config)
    
    try:
        with open(config_file, 'w') as f:
            json.dump(existing_config, f, indent=2)
        
        config_file.chmod(0o600)
    except IOError as e:
        raise ValueError(f"Failed to save configuration: {e}")


def save_api_key(api_key: str) -> None:
    save_config({'youtube_api_key': api_key})


def save_theme_preference(theme: str) -> None:
    save_config({'theme_preference': theme})


def setup_api_key_interactive() -> str: 
    print("\n🔑 YouTube API Key Setup")
    print("=" * 50)
    print("You need a YouTube Data API v3 key to use this application.")
    print("\nTo get your free API key:")
    print("1. Go to https://console.cloud.google.com/")
    print("2. Create a new project or select existing one")
    print("3. Enable the YouTube Data API v3")
    print("4. Create credentials (API key)")
    print("5. Copy your API key")
    print("\n" + "=" * 50)
    
    while True:
        api_key = getpass.getpass("Enter your YouTube API key: ").strip()
        if not api_key:
            print("❌ API key cannot be empty. Please try again.")
            continue
        
        if len(api_key) < 20:
            print("❌ API key seems too short. Please check and try again.")
            continue
        
        try:
            save_api_key(api_key)
            print("✅ API key saved successfully!")
            return api_key
        except ValueError as e:
            print(f"❌ Error saving API key: {e}")
            continue


def get_config_info() -> Dict:
    config_dir = _get_config_dir()
    config_file = _get_config_file()
    
    return {
        'config_dir': str(config_dir),
        'config_file': str(config_file),
        'config_exists': config_file.exists(),
        'config_dir_exists': config_dir.exists(),
    } 