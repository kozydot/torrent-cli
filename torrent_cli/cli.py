"""Command-line interface for the torrent CLI application."""

import sys
import argparse
from typing import Optional, Sequence
from colorama import Fore, Style

from .api_client import TorrentClient
from .download_manager import DownloadManager
from .progress import ProgressDisplay
from .error_handler import ErrorHandler, TorrentCliError
from .utils.validators import validate_search_query, validate_selection
from .utils.constants import (
    DEFAULT_SEARCH_LIMIT,
    EXIT_SUCCESS,
    MESSAGES,
    CATEGORIES,
    SORT_OPTIONS
)

class TorrentCLI:
    """Main CLI interface for the torrent application."""

    def __init__(self) -> None:
        """Initialize CLI components."""
        self.api_client = TorrentClient()
        self.download_manager = DownloadManager()
        self.progress = ProgressDisplay()

    def create_parser(self) -> argparse.ArgumentParser:
        """Create argument parser for CLI."""
        parser = argparse.ArgumentParser(
            description="A command-line interface for searching and downloading torrents",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  Search for torrents:
    %(prog)s search "ubuntu 22.04"
    %(prog)s search --limit 5 "python programming"
    %(prog)s search --category movies "inception"

  Download torrents:
    %(prog)s download "https://1337x.to/torrent/123456/ubuntu"
    %(prog)s download --name "custom-name" "magnet:?xt=urn:btih:..."
    %(prog)s download --dir "/downloads" "magnet:?xt=urn:btih:..."

  Other commands:
    %(prog)s trending                 # Show trending torrents
    %(prog)s trending --category movies --limit 5
    %(prog)s popular movies          # Show popular movie torrents
    %(prog)s top --category games    # Show top game torrents
            """
        )

        subparsers = parser.add_subparsers(dest="command", required=True)

        # Search command
        search_parser = subparsers.add_parser(
            "search",
            help="Search for torrents",
            description="Search for torrents with optional filters"
        )
        search_parser.add_argument(
            "query",
            help="Search query"
        )
        search_parser.add_argument(
            "-l", "--limit",
            type=int,
            default=DEFAULT_SEARCH_LIMIT,
            help=f"Maximum number of results (default: {DEFAULT_SEARCH_LIMIT})"
        )
        search_parser.add_argument(
            "-c", "--category",
            choices=CATEGORIES,
            help="Filter by category"
        )
        search_parser.add_argument(
            "-s", "--sort-by",
            choices=SORT_OPTIONS,
            help="Sort results by field"
        )
        search_parser.add_argument(
            "-o", "--order",
            choices=['desc', 'asc'],
            default='desc',
            help="Sort order (default: desc)"
        )

        # Download command
        download_parser = subparsers.add_parser(
            "download",
            help="Download a torrent by link",
            description="Download a torrent using a 1337x link or magnet link"
        )
        download_parser.add_argument(
            "link",
            help="1337x torrent link or magnet link"
        )
        download_parser.add_argument(
            "-n", "--name",
            help="Custom name for the torrent file"
        )
        download_parser.add_argument(
            "-d", "--dir",
            help="Custom download directory"
        )

        # Trending command
        trending_parser = subparsers.add_parser(
            "trending",
            help="Show trending torrents",
            description="Display currently trending torrents"
        )
        trending_parser.add_argument(
            "-c", "--category",
            choices=CATEGORIES,
            help="Filter by category"
        )
        trending_parser.add_argument(
            "-l", "--limit",
            type=int,
            default=DEFAULT_SEARCH_LIMIT,
            help=f"Maximum number of results (default: {DEFAULT_SEARCH_LIMIT})"
        )
        trending_parser.add_argument(
            "-w", "--week",
            action="store_true",
            help="Show weekly instead of daily trending"
        )

        # Popular command
        popular_parser = subparsers.add_parser(
            "popular",
            help="Show popular torrents by category",
            description="Display popular torrents in a specific category"
        )
        popular_parser.add_argument(
            "category",
            choices=CATEGORIES,
            help="Category to show popular torrents for"
        )
        popular_parser.add_argument(
            "-l", "--limit",
            type=int,
            default=DEFAULT_SEARCH_LIMIT,
            help=f"Maximum number of results (default: {DEFAULT_SEARCH_LIMIT})"
        )
        popular_parser.add_argument(
            "-w", "--week",
            action="store_true",
            help="Show weekly instead of daily popular"
        )

        # Top command
        top_parser = subparsers.add_parser(
            "top",
            help="Show top 100 torrents",
            description="Display top 100 torrents, optionally filtered by category"
        )
        top_parser.add_argument(
            "-c", "--category",
            choices=CATEGORIES,
            help="Filter by category"
        )
        top_parser.add_argument(
            "-l", "--limit",
            type=int,
            default=DEFAULT_SEARCH_LIMIT,
            help=f"Maximum number of results (default: {DEFAULT_SEARCH_LIMIT})"
        )

        return parser

    def search_torrents(self, query: str, limit: int = DEFAULT_SEARCH_LIMIT,
                       category: Optional[str] = None, sort_by: Optional[str] = None,
                       order: str = 'desc') -> None:
        """Search for torrents and display results."""
        try:
            # Validate and sanitize query
            query = validate_search_query(query)
            
            # Display banner and search status
            self.progress.show_banner()
            self.progress.info(MESSAGES["search_start"])
            
            # Perform search
            results = self.api_client.search(query, limit, category, sort_by, order)
            
            # Display results
            self.progress.display_search_results(results)
            
            # If results found, prompt for selection
            if results:
                self.handle_selection(results)

        except TorrentCliError as e:
            ErrorHandler.handle_error(e, exit_on_error=True)

    def handle_selection(self, results: list[dict]) -> None:
        """Handle user selection from search results."""
        try:
            # Prompt for selection
            selection = input(f"\n{Fore.CYAN}Enter the number of the torrent to download (or 'q' to quit): {Style.RESET_ALL}")
            
            if selection.lower() == 'q':
                sys.exit(EXIT_SUCCESS)

            # Validate selection
            index = validate_selection(selection, len(results))
            selected = results[index]

            # Get magnet link for selected torrent
            self.progress.info(MESSAGES["getting_magnet"])
            magnet = self.api_client.get_magnet(selected["link"])

            # Download selected torrent
            self.download_torrent(
                magnet,
                name=selected["name"]
            )

        except TorrentCliError as e:
            ErrorHandler.handle_error(e, exit_on_error=True)

    def download_torrent(self, link: str, name: Optional[str] = None) -> None:
        """Download a torrent file."""
        try:
            if link.startswith('magnet:'):
                # Direct magnet link download
                filepath = self.download_manager.download_torrent(link, name or "unnamed_torrent")
            else:
                # 1337x torrent link
                self.progress.info(MESSAGES["getting_magnet"])
                magnet = self.api_client.get_magnet(link)
                # Get name from API if not provided
                if not name:
                    info = self.api_client.get_torrent_info(link)
                    name = info.get('name', 'unnamed_torrent')
                filepath = self.download_manager.download_torrent(magnet, name)

            self.progress.display_download_status(filepath)
        except TorrentCliError as e:
            ErrorHandler.handle_error(e, exit_on_error=True)

    def show_trending(self, category: Optional[str] = None, week: bool = False,
                     limit: int = DEFAULT_SEARCH_LIMIT) -> None:
        """Show trending torrents."""
        try:
            self.progress.show_banner()
            self.progress.info(f"Getting {'weekly' if week else 'daily'} trending torrents...")
            results = self.api_client.trending(category, week)[:limit]
            self.progress.display_search_results(results)
            if results:
                self.handle_selection(results)
        except TorrentCliError as e:
            ErrorHandler.handle_error(e, exit_on_error=True)

    def show_popular(self, category: str, week: bool = False,
                    limit: int = DEFAULT_SEARCH_LIMIT) -> None:
        """Show popular torrents in a category."""
        try:
            self.progress.show_banner()
            self.progress.info(f"Getting {'weekly' if week else 'daily'} popular {category} torrents...")
            results = self.api_client.popular(category, week)[:limit]
            self.progress.display_search_results(results)
            if results:
                self.handle_selection(results)
        except TorrentCliError as e:
            ErrorHandler.handle_error(e, exit_on_error=True)

    def show_top(self, category: Optional[str] = None,
                 limit: int = DEFAULT_SEARCH_LIMIT) -> None:
        """Show top torrents."""
        try:
            self.progress.show_banner()
            self.progress.info(f"Getting top{f' {category}' if category else ''} torrents...")
            results = self.api_client.top(category)[:limit]
            self.progress.display_search_results(results)
            if results:
                self.handle_selection(results)
        except TorrentCliError as e:
            ErrorHandler.handle_error(e, exit_on_error=True)

    def run(self, args: Optional[Sequence[str]] = None) -> int:
        """Run the CLI application."""
        try:
            parser = self.create_parser()
            parsed_args = parser.parse_args(args)

            if parsed_args.command == "search":
                self.search_torrents(
                    parsed_args.query,
                    parsed_args.limit,
                    parsed_args.category,
                    parsed_args.sort_by,
                    parsed_args.order
                )
            elif parsed_args.command == "download":
                if parsed_args.dir:
                    self.download_manager = DownloadManager(parsed_args.dir)
                self.download_torrent(parsed_args.link, parsed_args.name)
            elif parsed_args.command == "trending":
                self.show_trending(parsed_args.category, parsed_args.week, parsed_args.limit)
            elif parsed_args.command == "popular":
                self.show_popular(parsed_args.category, parsed_args.week, parsed_args.limit)
            elif parsed_args.command == "top":
                self.show_top(parsed_args.category, parsed_args.limit)

            return EXIT_SUCCESS

        except KeyboardInterrupt:
            ErrorHandler.handle_keyboard_interrupt()
        except Exception as e:
            ErrorHandler.handle_error(e, exit_on_error=True)
            return 1  # This line won't be reached due to exit_on_error=True

def main() -> int:
    """Entry point for the application."""
    cli = TorrentCLI()
    return cli.run()

if __name__ == "__main__":
    sys.exit(main())