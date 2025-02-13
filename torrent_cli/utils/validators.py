"""Input validation and sanitization utilities."""

import os
import re
from typing import Union, Optional

from .constants import MIN_SEARCH_LENGTH, MAX_SEARCH_LENGTH, DOWNLOADS_DIR


class ValidationError(Exception):
    """Raised when input validation fails."""
    pass


def validate_search_query(query: str) -> str:
    """
    Validate and sanitize search query.

    Args:
        query (str): The search query to validate

    Returns:
        str: Sanitized search query

    Raises:
        ValidationError: If query is invalid
    """
    if not query or not isinstance(query, str):
        raise ValidationError("Search query must be a non-empty string")

    # Remove extra whitespace
    query = " ".join(query.split())

    if len(query) < MIN_SEARCH_LENGTH:
        raise ValidationError(f"Search query must be at least {MIN_SEARCH_LENGTH} characters")

    if len(query) > MAX_SEARCH_LENGTH:
        raise ValidationError(f"Search query must not exceed {MAX_SEARCH_LENGTH} characters")

    # Basic sanitization - remove special characters
    query = re.sub(r'[^a-zA-Z0-9\s-]', '', query)

    return query


def validate_selection(selection: Union[str, int], max_value: int) -> int:
    """
    Validate user selection from search results.

    Args:
        selection: User's selection (string or integer)
        max_value: Maximum allowed value

    Returns:
        int: Validated selection index

    Raises:
        ValidationError: If selection is invalid
    """
    try:
        index = int(selection)
        if not 1 <= index <= max_value:
            raise ValidationError(f"Selection must be between 1 and {max_value}")
        return index - 1  # Convert to 0-based index
    except ValueError:
        raise ValidationError("Selection must be a number")


def validate_download_path(path: Optional[str] = None) -> str:
    """
    Validate and create download directory if it doesn't exist.

    Args:
        path: Optional custom download path

    Returns:
        str: Validated download path

    Raises:
        ValidationError: If path is invalid or cannot be created
    """
    download_path = path or DOWNLOADS_DIR

    # Convert to absolute path
    download_path = os.path.abspath(download_path)

    # Check for directory traversal attempts
    if not os.path.normpath(download_path).startswith(os.getcwd()):
        raise ValidationError("Invalid download path")

    # Create directory if it doesn't exist
    try:
        os.makedirs(download_path, exist_ok=True)
    except OSError as e:
        raise ValidationError(f"Could not create download directory: {e}")

    # Verify write permissions
    if not os.access(download_path, os.W_OK):
        raise ValidationError("No write permission for download directory")

    return download_path


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to prevent path traversal and invalid characters.

    Args:
        filename: Original filename

    Returns:
        str: Sanitized filename
    """
    # Remove path separators and null bytes
    filename = os.path.basename(filename)
    filename = filename.replace('\0', '')

    # Remove or replace invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)

    # Limit length
    max_length = 255  # Maximum filename length for most filesystems
    if len(filename) > max_length:
        base, ext = os.path.splitext(filename)
        filename = base[:max_length - len(ext)] + ext

    return filename or "unnamed_torrent"  # Fallback if filename is empty