# 📹 flashback

A YouTube search tool that helps you find older content by searching videos from specific years. Available as both a Terminal User Interface (TUI - Thanks to [Textual](https://github.com/Textualize/textual)) and Command Line Interface (CLI).

# Demo

## TUI 



https://github.com/user-attachments/assets/b87dd093-f1f1-4c66-a75f-876af2fd8d46




## CLI

https://github.com/user-attachments/assets/cc1ff0cf-8b8b-48f7-8fce-ab78510ac59e

## Why?

YouTube's search filters are notoriously poor, especially when trying to find older content. The algorithm heavily favors newer videos, not surprisingly so, making it nearly impossible to discover gems from years past. This tool solves that problem by allowing you to search for videos from specific years (2005-2025).

## Features

-  **Search by specific year** - Find videos from any year (2005-2025)
-  **TUI interface** - Modern terminal interface with themes
-  **CLI mode** - Flags for power users and scripts
-  **Easy API key management** - Multiple ways to configure your YouTube API key
-  **Multiple themes** - Dark, light, gruvbox, dracula, nord, and more
-  **Direct video URLs** - Quick access to watch videos

## Installation

### pip, uv and poetry
```bash
# -- pip -- 
pip install ytflashback

# -- uv -- 
uv pip install ytflashback
# or
uv run --with ytflashback ytflashback

# -- poetry -- 
poetry add ytflashback 
```

### From Source
```bash
git clone https://github.com/cachebag/flashback.git
cd flashback
pip install -e .
```

## API Key Setup

You'll need a free YouTube Data API v3 key:

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the YouTube Data API v3
4. Create credentials (API key)
5. Copy your API key

### How to Configure Your API Key

#### Method 1: Standalone Command
```bash
ytflashback-api-key
```

#### Method 2: CLI Flag
```bash
ytflashback-cli --update-api-key
# or short form:
ytflashback-cli --api-key
```

#### Method 3: Interactive Mode
When using the CLI interface, type `api` to update your key:
```bash
ytflashback-cli
# Then type: api
```
If using the TUI, simply press `CTRL` + `K`

#### Method 4: Environment Variable
```bash
export YOUTUBE_API_KEY="key-goes-here"
```

## Usage

### TUI Mode (Default)
Launch the terminal interface:
```bash
ytflashback 
```

-  **Keyboard shortcuts:**
  - `Ctrl+S` - Search
  - `Ctrl+C` - Clear search
  - `Ctrl+T` - Toggle theme
  - `Ctrl+Shift+K` - Update API key
  - `Ctrl+Q` - Quit
  - `F1` - Help

### CLI Mode
For command-line usage and scripting:

#### Interactive CLI
```bash
ytflashback-cli
```

#### Direct Search
```bash
ytflashback-cli -q "python tutorial" -y 2019 -m 25
```

#### CLI Options
```bash
ytflashback-cli --help

Options:
  -q, --query TEXT             # YouTube search query
  -y, --year INTEGER           # Year to search for videos
  -m, --max-results INTEGER    # Maximum number of results (default: 25)
  --update-api-key, --api-key  # Update your YouTube API key and exit
  --help                       # Show this message and exit
```

## API Usage

- YouTube API has a daily quota of 10,000 units
- Each search uses ~100 units (≈100 searches/day)
- The API is free but rate-limited

## Development

### Setup Development Environment
```bash
git clone https://github.com/cachebag/flashback.git
cd flashback
pip install -e .
```

## Contributing

Feel free to submit issues and enhancement requests.

## LICENSE

This project is open source and available under the [MIT License](LICENSE). 
