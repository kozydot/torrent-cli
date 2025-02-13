"""Download manager for handling torrent file operations."""

import os
from typing import Optional
import requests

from .error_handler import DownloadError, ErrorHandler
from .progress import ProgressDisplay
from .utils.validators import validate_download_path, sanitize_filename
from .utils.constants import (
    DOWNLOADS_DIR,
    DEFAULT_CHUNK_SIZE,
    TORRENT_EXTENSION,
    MESSAGES
)

class DownloadManager:
    """Manages torrent file downloads and file system operations."""

    def __init__(self, download_dir: Optional[str] = None) -> None:
        """
        Initialize download manager.

        Args:
            download_dir: Optional custom download directory path
        
        Raises:
            DownloadError: If download directory setup fails
        """
        try:
            self.download_dir = validate_download_path(download_dir or DOWNLOADS_DIR)
            self.progress = ProgressDisplay()
        except Exception as e:
            raise DownloadError(f"Failed to initialize download manager: {e}")

    @ErrorHandler.wrap_errors(
        (requests.RequestException, OSError),
        custom_message="Download failed",
        exit_on_error=False
    )
    def download_torrent(self, magnet_link: str, name: str) -> str:
        """
        Download a torrent file from magnet link.

        Args:
            magnet_link: Magnet link for the torrent
            name: Name for the torrent file

        Returns:
            str: Path to the downloaded torrent file

        Raises:
            DownloadError: If download or file operations fail
        """
        # Sanitize filename and ensure .torrent extension
        filename = sanitize_filename(name)
        if not filename.endswith(TORRENT_EXTENSION):
            filename += TORRENT_EXTENSION

        filepath = os.path.join(self.download_dir, filename)

        try:
            # Create a placeholder .torrent file with the magnet link
            # In a real implementation, we would use libtorrent or similar
            # to convert the magnet link to an actual .torrent file
            self.progress.info(MESSAGES["download_start"])
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"d8:announce0:4:info{{\n")
                f.write(f"# This is a placeholder torrent file\n")
                f.write(f"# Magnet Link: {magnet_link}\n")
                f.write(f"# In a real implementation, this would be a proper .torrent file\n")
                f.write(f"}}e")

            return filepath

        except Exception as e:
            # Clean up partial download if it exists
            if os.path.exists(filepath):
                try:
                    os.remove(filepath)
                except OSError:
                    pass
            raise DownloadError(f"Failed to download torrent: {e}")

    def get_download_path(self) -> str:
        """
        Get the current download directory path.

        Returns:
            str: Path to download directory
        """
        return self.download_dir