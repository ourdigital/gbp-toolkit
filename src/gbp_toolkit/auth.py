"""
Authentication module for Google Business Profile API
"""

import json
import os
from typing import Optional, Dict, Any
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from dotenv import load_dotenv

from .exceptions import GBPAuthError

# Load environment variables
load_dotenv()


class GBPAuth:
    """Handles authentication for Google Business Profile API"""
    
    SCOPES = [
        'https://www.googleapis.com/auth/business.manage'
    ]
    
    def __init__(self, credentials_file: Optional[str] = None, token_file: Optional[str] = None):
        """
        Initialize GBP authentication
        
        Args:
            credentials_file: Path to OAuth2 credentials JSON file
            token_file: Path to store/load access tokens
        """
        self.credentials_file = (
            credentials_file or 
            os.getenv('GBP_CREDENTIALS_FILE') or 
            'credentials.json'
        )
        self.token_file = (
            token_file or 
            os.getenv('GBP_TOKEN_FILE') or 
            'token.json'
        )
        self.credentials: Optional[Credentials] = None
        
    def authenticate(self, redirect_uri: Optional[str] = None) -> Credentials:
        """
        Perform OAuth2 authentication flow
        
        Args:
            redirect_uri: OAuth redirect URI
            
        Returns:
            Google OAuth2 credentials
            
        Raises:
            GBPAuthError: If authentication fails
        """
        # Use environment variable for redirect URI if not provided
        if redirect_uri is None:
            redirect_uri = os.getenv('GBP_REDIRECT_URI', 'http://localhost:8080/callback')
            
        try:
            # Try to load existing token
            if os.path.exists(self.token_file):
                self.credentials = Credentials.from_authorized_user_file(self.token_file, self.SCOPES)
            
            # If there are no valid credentials available, let the user log in
            if not self.credentials or not self.credentials.valid:
                if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                    self.credentials.refresh(Request())
                else:
                    if not os.path.exists(self.credentials_file):
                        raise GBPAuthError(f"Credentials file not found: {self.credentials_file}")
                    
                    flow = Flow.from_client_secrets_file(
                        self.credentials_file, 
                        scopes=self.SCOPES,
                        redirect_uri=redirect_uri
                    )
                    
                    # Get the authorization URL
                    auth_url, _ = flow.authorization_url(prompt='consent')
                    
                    print(f"Please go to this URL and authorize the application: {auth_url}")
                    code = input("Enter the authorization code: ")
                    
                    # Exchange the code for credentials
                    flow.fetch_token(code=code)
                    self.credentials = flow.credentials
                
                # Save the credentials for the next run
                self._save_credentials()
            
            return self.credentials
            
        except Exception as e:
            raise GBPAuthError(f"Authentication failed: {str(e)}")
    
    def _save_credentials(self):
        """Save credentials to token file"""
        try:
            with open(self.token_file, 'w') as token:
                token.write(self.credentials.to_json())
        except Exception as e:
            raise GBPAuthError(f"Failed to save credentials: {str(e)}")
    
    def get_service(self, service_name: str = 'mybusiness', version: str = 'v4'):
        """
        Get authenticated Google API service
        
        Args:
            service_name: Name of the Google service
            version: API version
            
        Returns:
            Authenticated Google API service object
        """
        if not self.credentials:
            raise GBPAuthError("Not authenticated. Call authenticate() first.")
        
        return build(service_name, version, credentials=self.credentials)
    
    def revoke_credentials(self):
        """Revoke and remove stored credentials"""
        if self.credentials:
            self.credentials.revoke(Request())
        
        if os.path.exists(self.token_file):
            os.remove(self.token_file)
        
        self.credentials = None