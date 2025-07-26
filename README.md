# 📹 flashback

A CLI tool for searching YouTube videos by specific year, helping you discover older content that might be buried by YouTube's algorithm favoring newer videos.

## Why?
YouTube's search filters are notoriously poor, especially when trying to find older content. Even though there's a wealth of YouTube videos buried deep in the site, we often can't find them because only the newest ones show up in search results (I believe at any given time you can only see videos from the past year). This tool solves that problem by allowing you to search for videos from specific years. 

## Features

- Search YouTube videos by specific year
- Display results in a clean, formatted table
- Get direct video URLs 

## Setup

### Prerequisites

- Python 3.7 or higher
- YouTube Data API v3 key

### You'll need a YouTube Data API v3 Key (it's free)

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the YouTube Data API v3
4. Create credentials (API key)
5. Copy your API key in your `.env` file in the root of the project

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the MIT License. 