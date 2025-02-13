"""Error handling utilities for the torrent CLI application."""

import sys
import logging
import traceback
from typing import Type, Optional
from colorama import Fore, Style, init

from .utils.constants import EXIT_FAILURE, MESSAGES

# Initialize colorama
init(autoreset=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='torrent_cli.log'
)
logger = logging.getLogger(__name__)

class TorrentCliError(Exception):
    """Base exception class for torrent CLI application."""
    def __init__(self, message: str, error_type: str = "Error"):
        self.message = message
        self.error_type = error_type
        super().__init__(self.message)

class APIError(TorrentCliError):
    """Raised when API interaction fails."""
    def __init__(self, message: str):
        super().__init__(message, "API Error")

class DownloadError(TorrentCliError):
    """Raised when download operation fails."""
    def __init__(self, message: str):
        super().__init__(message, "Download Error")

class ValidationError(TorrentCliError):
    """Raised when input validation fails."""
    def __init__(self, message: str):
        super().__init__(message, "Validation Error")

class ConnectionError(TorrentCliError):
    """Raised when network connection fails."""
    def __init__(self, message: str):
        super().__init__(message, "Connection Error")

class ErrorHandler:
    """Handles error cases and provides user-friendly messages."""

    ERROR_COLORS = {
        "API Error": Fore.RED,
        "Download Error": Fore.YELLOW,
        "Validation Error": Fore.MAGENTA,
        "Connection Error": Fore.CYAN,
        "Error": Fore.RED
    }

    @classmethod
    def format_error(cls, error: Exception) -> str:
        """Format error message with color and type."""
        if isinstance(error, TorrentCliError):
            color = cls.ERROR_COLORS.get(error.error_type, Fore.RED)
            return f"\n{color}[{error.error_type}]{Style.RESET_ALL} {error.message}"
        return f"\n{Fore.RED}[Error]{Style.RESET_ALL} {str(error)}"

    @classmethod
    def handle_error(
        cls,
        error: Exception,
        exit_on_error: bool = True,
        show_traceback: bool = False
    ) -> None:
        """
        Handle an error with appropriate logging and user feedback.

        Args:
            error: The exception to handle
            exit_on_error: Whether to exit the program after handling
            show_traceback: Whether to show the full traceback (debug only)
        """
        # Format and display error message
        error_message = cls.format_error(error)
        print(error_message)

        # Log the error with traceback
        logger.error(
            error_message,
            exc_info=True,
            extra={
                "error_type": error.__class__.__name__,
                "error_message": str(error)
            }
        )

        if show_traceback:
            print(f"\n{Fore.YELLOW}Traceback:{Style.RESET_ALL}")
            traceback.print_exc()

        # Add helpful hints based on error type
        if isinstance(error, ValidationError):
            print(f"\n{Fore.CYAN}💡 Hint: {MESSAGES['validation_error'].format(str(error))}{Style.RESET_ALL}")
        elif isinstance(error, ConnectionError):
            print(f"\n{Fore.CYAN}💡 Hint: {MESSAGES['connection_error']}{Style.RESET_ALL}")
        elif isinstance(error, APIError):
            print(f"\n{Fore.CYAN}💡 Hint: {MESSAGES['api_error']}{Style.RESET_ALL}")

        if exit_on_error:
            sys.exit(EXIT_FAILURE)

    @staticmethod
    def handle_keyboard_interrupt() -> None:
        """Handle keyboard interrupt (Ctrl+C) gracefully."""
        print(f"\n{Fore.YELLOW}{MESSAGES['keyboard_interrupt']}{Style.RESET_ALL}")
        sys.exit(130)  # Standard exit code for keyboard interrupt

    @classmethod
    def wrap_errors(
        cls,
        error_types: tuple[Type[Exception], ...],
        custom_message: Optional[str] = None,
        exit_on_error: bool = True
    ):
        """
        Decorator to wrap function calls with error handling.

        Args:
            error_types: Tuple of exception types to catch
            custom_message: Optional custom error message
            exit_on_error: Whether to exit the program after handling

        Returns:
            Decorated function
        """
        def decorator(func):
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except error_types as e:
                    message = custom_message or str(e)
                    wrapped_error = TorrentCliError(message)
                    cls.handle_error(wrapped_error, exit_on_error=exit_on_error)
                except KeyboardInterrupt:
                    cls.handle_keyboard_interrupt()
            return wrapper
        return decorator