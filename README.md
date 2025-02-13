# Torrent CLI

A feature-rich command-line interface for searching and downloading torrents from 1337x.

## Features

- Advanced torrent search with filters and sorting
- Trending, popular, and top torrent listings
- Beautiful colorized output with progress tracking
- Smart proxy management with automatic failover
- Automatic download directory management
- Comprehensive error handling
- Cache support for faster responses
- Dynamic terminal width adaptation
- Emoji-enhanced user interface

## Installation

1. Clone the repository:
```bash
git clone https://github.com/kozydot/torrent-cli.git
cd torrent-cli
```

2. Install the package:
```bash
pip install -e .
```

## Usage

### Search for torrents:
```bash
# Basic search
torrent-cli search "ubuntu 22.04"

# With limit and category
torrent-cli search "inception" --limit 5 --category movies

# With sorting
torrent-cli search "python" --sort-by seeders --order desc
```

### Download torrents:
```bash
# Download using magnet link
torrent-cli download "magnet:?xt=urn:btih:..."

# Download with custom name
torrent-cli download --name "custom-name" "https://1337x.to/torrent/123456/"

# Download to specific directory
torrent-cli download --dir "/downloads" "magnet:?xt=urn:btih:..."
```

### Trending torrents:
```bash
# Show all trending
torrent-cli trending

# Category-specific trending with limit
torrent-cli trending --category movies --limit 5

# Weekly trending
torrent-cli trending --week
```

### Popular torrents:
```bash
# Show popular in category
torrent-cli popular movies

# Weekly popular with limit
torrent-cli popular games --week --limit 10
```

### Top torrents:
```bash
# Show top torrents
torrent-cli top

# Category-specific top with limit
torrent-cli top --category anime --limit 5
```

## Available Categories

- movies
- tv
- games
- music
- apps
- anime
- documentaries
- xxx
- others

## Sort Options

- time
- size
- seeders
- leechers

## Configuration

The CLI automatically manages:
- Download directory creation
- Proxy selection and failover
- Cache management
- Terminal width adaptation

## Error Handling

The application includes error handling for:
- Network connectivity issues
- API communication problems
- Invalid user input
- File system operations
- Proxy failures
- Rate limiting

## Development

1. Set up development environment:
```bash
pip install -e ".[dev]"
```

2. Run tests:
```bash
pytest
```

## Project Structure

```
torrent_cli/
├── __init__.py         # Package initialization
├── __main__.py        # Module entry point
├── cli.py             # Main CLI interface
├── api_client.py      # 1337x API client
├── download_manager.py # Download handling
├── error_handler.py   # Error management
├── progress.py        # Progress display
└── utils/            # Utility modules
    ├── __init__.py
    ├── constants.py  # Configuration constants
    └── validators.py # Input validation
```

## Dependencies

- 1337x: API wrapper for 1337x
- colorama: Cross-platform colored terminal output
- tqdm: Progress bar functionality
- requests: HTTP client library
- beautifulsoup4: HTML parsing
- requests-cache: Response caching
- cloudscraper: Cloudflare bypass
- pytest: Testing framework

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Known Issues

- Some proxies may be temporarily unavailable
- Cloudflare protection may require retries
- Large result sets may take longer to process

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is for educational purposes only. Be sure to comply with your local laws and regulations regarding torrent downloads.

## Acknowledgments

- 1337x for the torrent data
- Contributors to the dependency packages
- The open-source community

---
Made with ❤️ by kozydot
