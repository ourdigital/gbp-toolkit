"""
GBP Toolkit - A Python toolkit for managing Google Business Profile via GBP APIs
"""

__version__ = "0.1.0"
__author__ = "GBP Toolkit"

from .client import GBPClient
from .auth import GBPAuth
from .business_profile import BusinessProfileManager
from .exceptions import GBPError, GBPAuthError, GBPAPIError

__all__ = ["GBPClient", "GBPAuth", "BusinessProfileManager", "GBPError", "GBPAuthError", "GBPAPIError"]