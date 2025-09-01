"""
Custom exceptions for GBP Toolkit
"""


class GBPError(Exception):
    """Base exception for GBP Toolkit"""
    pass


class GBPAuthError(GBPError):
    """Authentication related errors"""
    pass


class GBPAPIError(GBPError):
    """API request/response related errors"""
    def __init__(self, message, status_code=None, response=None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response