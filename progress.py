"""Progress tracking and status display utilities."""

import os
from typing import Optional, Any
from colorama import Fore, Style, init
from tqdm import tqdm

from .utils.constants import COLORS, MESSAGES

# Initialize colorama
init(autoreset=True)

class ProgressDisplay:
    """Handles progress bars and status messages with colored output."""

    BANNER = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗
║                   {Fore.WHITE}1337x Torrent Search CLI{Fore.CYAN}                   ║
╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
    """

    @staticmethod
    def _get_color(color_name: str) -> str:
        """Get ANSI color code from color name."""
        return getattr(Fore, COLORS[color_name].upper())

    @classmethod
    def show_banner(cls) -> None:
        """Display the CLI banner."""
        print(cls.BANNER)

    @classmethod
    def info(cls, message: str) -> None:
        """Display info message in blue."""
        color = cls._get_color("info")
        print(f"{color}ℹ {message}{Style.RESET_ALL}")

    @classmethod
    def success(cls, message: str) -> None:
        """Display success message in green."""
        color = cls._get_color("success")
        print(f"{color}✔ {message}{Style.RESET_ALL}")

    @classmethod
    def warning(cls, message: str) -> None:
        """Display warning message in yellow."""
        color = cls._get_color("warning")
        print(f"{color}⚠ {message}{Style.RESET_ALL}")

    @classmethod
    def error(cls, message: str) -> None:
        """Display error message in red."""
        color = cls._get_color("error")
        print(f"{color}✘ {message}{Style.RESET_ALL}")

    @staticmethod
    def progress_bar(
        total: int,
        desc: Optional[str] = None,
        unit: str = "B",
        unit_scale: bool = True,
        **kwargs: Any
    ) -> tqdm:
        """
        Create a progress bar for tracking downloads.

        Args:
            total: Total size/steps
            desc: Description text
            unit: Unit of measurement
            unit_scale: Whether to scale units automatically
            **kwargs: Additional arguments for tqdm

        Returns:
            tqdm: Progress bar instance
        """
        return tqdm(
            total=total,
            desc=desc,
            unit=unit,
            unit_scale=unit_scale,
            ncols=80,
            bar_format="{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]",
            colour=COLORS["progress"],
            **kwargs
        )

    @classmethod
    def display_search_results(cls, results: list[dict]) -> None:
        """
        Display search results in a formatted table.

        Args:
            results: List of torrent search results
        """
        if not results:
            cls.warning(MESSAGES["no_results"])
            return

        # Calculate column widths based on terminal size
        terminal_width = os.get_terminal_size().columns
        name_width = terminal_width - 35  # Reserve space for other columns
        size_width = 10
        seeders_width = 8
        leechers_width = 8
        total_width = name_width + size_width + seeders_width + leechers_width + 5

        # Print header
        print()
        header = (
            f"{Fore.CYAN}{'#':<4} "
            f"{'Name':<{name_width}} "
            f"{'Size':<{size_width}} "
            f"{'↑':<{seeders_width}} "
            f"{'↓':<{leechers_width}}{Style.RESET_ALL}"
        )
        print(header)
        print(f"{Fore.BLUE}{'-' * total_width}{Style.RESET_ALL}")

        # Print results
        for i, torrent in enumerate(results, 1):
            name = torrent['name']
            if len(name) > name_width - 3:
                name = name[:name_width - 3] + "..."

            row = (
                f"{Fore.GREEN}{i:<4}{Style.RESET_ALL} "
                f"{name:<{name_width}} "
                f"{torrent['size']:<{size_width}} "
                f"{Fore.GREEN}{torrent['seeders']:<{seeders_width}}{Style.RESET_ALL} "
                f"{Fore.RED}{torrent['leechers']:<{leechers_width}}{Style.RESET_ALL}"
            )
            print(row)
        print()

    @classmethod
    def display_download_status(cls, filepath: str, status: str = "success") -> None:
        """
        Display download completion status.

        Args:
            filepath: Path to the downloaded file
            status: Status type ('success' or 'error')
        """
        # Get terminal width for path truncation
        terminal_width = os.get_terminal_size().columns
        max_path_length = terminal_width - 10

        # Format the status message
        if status == "success":
            cls.success(MESSAGES["download_complete"])
            
            # Truncate path if too long
            display_path = filepath
            if len(display_path) > max_path_length:
                display_path = "..." + filepath[-(max_path_length-3):]
            
            print(f"{Fore.CYAN}📁 {display_path}{Style.RESET_ALL}")
        else:
            cls.error(f"{MESSAGES['download_error']} ({filepath})")