"""Constants used throughout the torrent CLI application."""

# File system
DOWNLOADS_DIR = "downloads"
DEFAULT_CHUNK_SIZE = 8192  # bytes

# API settings
DEFAULT_SEARCH_LIMIT = 10
API_TIMEOUT = 30  # seconds
MAX_RETRIES = 3
RETRY_DELAY = 1  # seconds

# Input validation
MIN_SEARCH_LENGTH = 3
MAX_SEARCH_LENGTH = 100

# Display settings
COLORS = {
    "success": "green",
    "error": "red",
    "warning": "yellow",
    "info": "blue",
    "progress": "cyan"
}

# Categories
CATEGORIES = [
    'movies',
    'tv',
    'games',
    'music',
    'apps',
    'anime',
    'documentaries',
    'xxx',
    'others'
]

# Sort options
SORT_OPTIONS = [
    'time',
    'size',
    'seeders',
    'leechers'
]

# Status messages
MESSAGES = {
    "search_start": "🔍 Searching for torrents...",
    "no_results": "😕 No torrents found for the given query.",
    "download_start": "📥 Starting download...",
    "download_complete": "✅ Download completed successfully!",
    "download_error": "❌ Failed to download torrent file.",
    "invalid_input": "⚠️ Invalid input. Please try again.",
    "api_error": "🚫 Error communicating with the API. Please try again.",
    "creating_dir": "📁 Creating downloads directory...",
    "dir_exists": "📂 Downloads directory already exists.",
    "getting_magnet": "🧲 Getting magnet link...",
    "getting_info": "ℹ️ Getting torrent information...",
    "keyboard_interrupt": "\n⚠️ Operation cancelled by user",
    "connection_error": "🌐 Connection error. Please check your internet connection.",
    "rate_limit": "⏳ Rate limit reached. Please wait a moment and try again.",
    "proxy_error": "🔄 Current proxy failed, trying another one...",
    "validation_error": "⚠️ Validation error: {}"
}

# File extensions
TORRENT_EXTENSION = ".torrent"

# Exit codes
EXIT_SUCCESS = 0
EXIT_FAILURE = 1
EXIT_KEYBOARD_INTERRUPT = 130

# Help messages
CATEGORY_HELP = """
Available Categories:
  movies        - Movie torrents
  tv           - TV show torrents
  games        - Game torrents
  music        - Music torrents
  apps         - Application torrents
  anime        - Anime torrents
  documentaries - Documentary torrents
  xxx          - Adult content torrents
  others       - Other torrents
"""

SORT_HELP = """
Sort Options:
  time     - Sort by upload time
  size     - Sort by file size
  seeders  - Sort by number of seeders
  leechers - Sort by number of leechers
"""

ORDER_HELP = """
Sort Order:
  desc - Descending order (default)
  asc  - Ascending order
"""