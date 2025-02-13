"""API client for interacting with the 1337x torrent service."""

import time
import logging
import re
from typing import List, Dict, Any, Optional
from py1337x import py1337x

from .error_handler import APIError, ErrorHandler
from .utils.constants import (
    API_TIMEOUT,
    MAX_RETRIES,
    RETRY_DELAY,
    DEFAULT_SEARCH_LIMIT
)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class TorrentClient:
    """Client for interacting with 1337x API."""

    PROXIES = [
        '1337x.to',
        'x1337x.se',
        'x1337x.ws',
        'x1337x.eu'
    ]

    def __init__(self) -> None:
        """Initialize the torrent client."""
        self.client = None
        self._initialize_client()

    def _initialize_client(self) -> None:
        """Initialize client with working proxy."""
        for proxy in self.PROXIES:
            try:
                logger.debug(f"Trying proxy: {proxy}")
                self.client = py1337x(
                    proxy=proxy,
                    cache=True,
                    cacheTime=300
                )
                # Test the connection
                test = self.client.trending()
                if test and isinstance(test, dict) and 'items' in test:
                    logger.debug(f"Successfully connected using proxy: {proxy}")
                    return
            except Exception as e:
                logger.warning(f"Failed to initialize with proxy {proxy}: {e}")
                continue

        raise APIError("Failed to initialize API client with any proxy")

    def _extract_torrent_id(self, url: str) -> str:
        """Extract torrent ID from URL."""
        patterns = [
            r'1337x\.to/torrent/(\d+)',
            r'x1337x\.[^/]+/torrent/(\d+)',
            r'/torrent/(\d+)'
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)

        raise APIError(f"Could not extract torrent ID from URL: {url}")

    def search(self, query: str, limit: int = DEFAULT_SEARCH_LIMIT,
              category: Optional[str] = None, sort_by: Optional[str] = None,
              order: str = 'desc') -> List[Dict[str, Any]]:
        """Search for torrents."""
        try:
            logger.debug(f"Searching for query: {query} (limit: {limit})")
            
            # Perform the search
            response = self.client.search(query, category=category, sortBy=sort_by, order=order)
            logger.debug(f"Search response: {response}")

            if not response or not isinstance(response, dict) or 'items' not in response:
                logger.warning("No valid items found in search response")
                return []

            # Get the first 'limit' results
            results = response['items'][:limit]
            logger.debug(f"Processing {len(results)} results")

            processed_results = []
            for result in results:
                try:
                    # Get info directly using the link instead of torrent ID
                    info = self.get_torrent_info(result['link'])
                    processed_results.append({
                        "name": info.get('name', result['name']),
                        "size": info.get('size', result['size']),
                        "seeders": info.get('seeders', result['seeders']),
                        "leechers": info.get('leechers', result['leechers']),
                        "magnet": info.get('magnetLink', ''),
                        "link": result['link']
                    })
                except KeyError as e:
                    logger.error(f"Missing key in result: {e}")
                    continue
                except Exception as e:
                    logger.error(f"Failed to process result: {e}")
                    continue

            return processed_results

        except Exception as e:
            logger.error(f"Search failed: {e}")
            raise APIError(f"Failed to search torrents: {e}")

    def trending(self, category: Optional[str] = None, week: bool = False) -> List[Dict[str, Any]]:
        """Get trending torrents."""
        try:
            logger.debug(f"Getting trending torrents (category: {category}, week: {week})")
            response = self.client.trending(category=category, week=week)
            
            if not response or not isinstance(response, dict) or 'items' not in response:
                logger.warning("No valid items found in trending response")
                return []

            results = response['items']
            processed_results = []

            for result in results:
                try:
                    info = self.get_torrent_info(result['link'])
                    processed_results.append({
                        "name": info.get('name', result['name']),
                        "size": info.get('size', result['size']),
                        "seeders": info.get('seeders', result['seeders']),
                        "leechers": info.get('leechers', result['leechers']),
                        "magnet": info.get('magnetLink', ''),
                        "link": result['link']
                    })
                except Exception as e:
                    logger.error(f"Failed to process trending result: {e}")
                    continue

            return processed_results

        except Exception as e:
            logger.error(f"Trending request failed: {e}")
            raise APIError(f"Failed to get trending torrents: {e}")

    def popular(self, category: str, week: bool = False) -> List[Dict[str, Any]]:
        """Get popular torrents."""
        try:
            logger.debug(f"Getting popular torrents (category: {category}, week: {week})")
            response = self.client.popular(category=category, week=week)
            
            if not response or not isinstance(response, dict) or 'items' not in response:
                logger.warning("No valid items found in popular response")
                return []

            results = response['items']
            processed_results = []

            for result in results:
                try:
                    info = self.get_torrent_info(result['link'])
                    processed_results.append({
                        "name": info.get('name', result['name']),
                        "size": info.get('size', result['size']),
                        "seeders": info.get('seeders', result['seeders']),
                        "leechers": info.get('leechers', result['leechers']),
                        "magnet": info.get('magnetLink', ''),
                        "link": result['link']
                    })
                except Exception as e:
                    logger.error(f"Failed to process popular result: {e}")
                    continue

            return processed_results

        except Exception as e:
            logger.error(f"Popular request failed: {e}")
            raise APIError(f"Failed to get popular torrents: {e}")

    def top(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get top torrents."""
        try:
            logger.debug(f"Getting top torrents (category: {category})")
            response = self.client.top(category=category)
            
            if not response or not isinstance(response, dict) or 'items' not in response:
                logger.warning("No valid items found in top response")
                return []

            results = response['items']
            processed_results = []

            for result in results:
                try:
                    info = self.get_torrent_info(result['link'])
                    processed_results.append({
                        "name": info.get('name', result['name']),
                        "size": info.get('size', result['size']),
                        "seeders": info.get('seeders', result['seeders']),
                        "leechers": info.get('leechers', result['leechers']),
                        "magnet": info.get('magnetLink', ''),
                        "link": result['link']
                    })
                except Exception as e:
                    logger.error(f"Failed to process top result: {e}")
                    continue

            return processed_results

        except Exception as e:
            logger.error(f"Top request failed: {e}")
            raise APIError(f"Failed to get top torrents: {e}")

    def get_torrent_info(self, link: str) -> Dict[str, Any]:
        """Get detailed information about a torrent."""
        try:
            logger.debug(f"Getting torrent info for: {link}")
            
            # Always use the full link instead of torrent ID
            if not link.startswith('http'):
                # If we have an ID, construct the full URL
                link = f"{self.client.baseUrl}/torrent/{link}/"
            
            info = self.client.info(link=link)
            
            if not info or not isinstance(info, dict):
                raise APIError("Invalid torrent info response")
                
            logger.debug(f"Got torrent info: {info}")
            return info

        except Exception as e:
            logger.error(f"Failed to get torrent info: {e}")
            raise APIError(f"Failed to get torrent info: {e}")

    def get_magnet(self, link: str) -> str:
        """Get magnet link for a torrent."""
        try:
            logger.debug(f"Getting magnet link for: {link}")
            info = self.get_torrent_info(link)
            magnet = info.get('magnetLink')
            if not magnet:
                raise APIError("No magnet link found in torrent info")
            return magnet
        except Exception as e:
            logger.error(f"Failed to get magnet link: {e}")
            raise APIError(f"Failed to get magnet link: {e}")