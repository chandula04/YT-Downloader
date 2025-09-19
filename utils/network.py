"""
Network utilities for HTTP requests and session management
"""

import requests
import urllib3
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from config.settings import (
    MAX_RETRIES, RETRY_BACKOFF_FACTOR, REQUEST_TIMEOUT,
    POOL_CONNECTIONS, POOL_MAX_SIZE, RETRY_STATUS_CODES, DEFAULT_HEADERS
)

# Disable insecure request warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class NetworkManager:
    """Manages HTTP sessions with retry logic and proper configuration"""
    
    def __init__(self):
        self._session = None
    
    def create_session(self):
        """
        Create a requests session with retries and custom settings
        
        Returns:
            requests.Session: Configured session with retry logic
        """
        session = requests.Session()
        
        # Configure retries
        retry_strategy = Retry(
            total=MAX_RETRIES,
            backoff_factor=RETRY_BACKOFF_FACTOR,
            status_forcelist=RETRY_STATUS_CODES,
        )
        
        adapter = HTTPAdapter(
            max_retries=retry_strategy, 
            pool_connections=POOL_CONNECTIONS, 
            pool_maxsize=POOL_MAX_SIZE
        )
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        # Set longer timeouts
        session.timeout = REQUEST_TIMEOUT
        
        self._session = session
        return session
    
    def get_session(self):
        """
        Get the current session, create one if it doesn't exist
        
        Returns:
            requests.Session: Current session
        """
        if self._session is None:
            return self.create_session()
        return self._session
    
    def get_headers(self):
        """
        Return headers that mimic a web browser
        
        Returns:
            dict: HTTP headers
        """
        return DEFAULT_HEADERS.copy()
    
    def close_session(self):
        """Close the current session"""
        if self._session:
            self._session.close()
            self._session = None


# Global network manager instance
network_manager = NetworkManager()