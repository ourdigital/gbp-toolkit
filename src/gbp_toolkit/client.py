"""
Core client for Google Business Profile API operations
"""

from typing import List, Dict, Any, Optional
from googleapiclient.errors import HttpError

from .auth import GBPAuth
from .exceptions import GBPAPIError


class GBPClient:
    """Main client for Google Business Profile API operations"""
    
    def __init__(self, auth: Optional[GBPAuth] = None):
        """
        Initialize GBP client
        
        Args:
            auth: GBPAuth instance (creates new one if not provided)
        """
        self.auth = auth or GBPAuth()
        self.service = None
        self.performance_service = None
        
    def authenticate(self, credentials_file: Optional[str] = None, 
                    token_file: Optional[str] = None, 
                    redirect_uri: str = 'http://localhost:8080/callback'):
        """
        Authenticate with Google Business Profile API
        
        Args:
            credentials_file: Path to OAuth2 credentials JSON file
            token_file: Path to store/load access tokens  
            redirect_uri: OAuth redirect URI
        """
        if credentials_file:
            self.auth.credentials_file = credentials_file
        if token_file:
            self.auth.token_file = token_file
            
        self.auth.authenticate(redirect_uri)
        self.service = self.auth.get_service('mybusiness', 'v4')
        self.performance_service = self.auth.get_service('businessprofileperformance', 'v1')
    
    def _handle_api_error(self, error: HttpError) -> None:
        """Handle API errors and convert to GBPAPIError"""
        try:
            error_detail = error.error_details[0] if error.error_details else {}
            message = error_detail.get('message', str(error))
        except:
            message = str(error)
        
        raise GBPAPIError(
            message=message,
            status_code=error.resp.status,
            response=error.content
        )
    
    def list_accounts(self) -> List[Dict[str, Any]]:
        """
        List all Google Business Profile accounts
        
        Returns:
            List of account dictionaries
            
        Raises:
            GBPAPIError: If API request fails
        """
        if not self.service:
            raise GBPAPIError("Not authenticated. Call authenticate() first.")
        
        try:
            result = self.service.accounts().list().execute()
            return result.get('accounts', [])
        except HttpError as e:
            self._handle_api_error(e)
    
    def get_account(self, account_name: str) -> Dict[str, Any]:
        """
        Get specific account details
        
        Args:
            account_name: Account resource name (e.g., 'accounts/123')
            
        Returns:
            Account dictionary
            
        Raises:
            GBPAPIError: If API request fails
        """
        if not self.service:
            raise GBPAPIError("Not authenticated. Call authenticate() first.")
        
        try:
            return self.service.accounts().get(name=account_name).execute()
        except HttpError as e:
            self._handle_api_error(e)
    
    def list_locations(self, account_name: str, page_size: int = 100) -> List[Dict[str, Any]]:
        """
        List all locations for an account
        
        Args:
            account_name: Account resource name (e.g., 'accounts/123')
            page_size: Number of locations to return per page
            
        Returns:
            List of location dictionaries
            
        Raises:
            GBPAPIError: If API request fails
        """
        if not self.service:
            raise GBPAPIError("Not authenticated. Call authenticate() first.")
        
        try:
            locations = []
            request = self.service.accounts().locations().list(
                parent=account_name,
                pageSize=page_size
            )
            
            while request is not None:
                result = request.execute()
                locations.extend(result.get('locations', []))
                request = self.service.accounts().locations().list_next(request, result)
            
            return locations
        except HttpError as e:
            self._handle_api_error(e)
    
    def get_location(self, location_name: str) -> Dict[str, Any]:
        """
        Get specific location details
        
        Args:
            location_name: Location resource name (e.g., 'accounts/123/locations/456')
            
        Returns:
            Location dictionary
            
        Raises:
            GBPAPIError: If API request fails
        """
        if not self.service:
            raise GBPAPIError("Not authenticated. Call authenticate() first.")
        
        try:
            return self.service.accounts().locations().get(name=location_name).execute()
        except HttpError as e:
            self._handle_api_error(e)
    
    def update_location(self, location_name: str, location_data: Dict[str, Any], 
                       update_mask: Optional[str] = None) -> Dict[str, Any]:
        """
        Update location information
        
        Args:
            location_name: Location resource name
            location_data: Updated location data
            update_mask: Fields to update (comma-separated)
            
        Returns:
            Updated location dictionary
            
        Raises:
            GBPAPIError: If API request fails
        """
        if not self.service:
            raise GBPAPIError("Not authenticated. Call authenticate() first.")
        
        try:
            params = {'name': location_name, 'body': location_data}
            if update_mask:
                params['updateMask'] = update_mask
            
            return self.service.accounts().locations().patch(**params).execute()
        except HttpError as e:
            self._handle_api_error(e)
    
    def list_reviews(self, location_name: str, page_size: int = 50) -> List[Dict[str, Any]]:
        """
        List reviews for a location
        
        Args:
            location_name: Location resource name
            page_size: Number of reviews to return per page
            
        Returns:
            List of review dictionaries
            
        Raises:
            GBPAPIError: If API request fails
        """
        if not self.service:
            raise GBPAPIError("Not authenticated. Call authenticate() first.")
        
        try:
            reviews = []
            request = self.service.accounts().locations().reviews().list(
                parent=location_name,
                pageSize=page_size
            )
            
            while request is not None:
                result = request.execute()
                reviews.extend(result.get('reviews', []))
                request = self.service.accounts().locations().reviews().list_next(request, result)
            
            return reviews
        except HttpError as e:
            self._handle_api_error(e)
    
    def reply_to_review(self, review_name: str, comment: str) -> Dict[str, Any]:
        """
        Reply to a customer review
        
        Args:
            review_name: Review resource name
            comment: Reply comment text
            
        Returns:
            Review reply dictionary
            
        Raises:
            GBPAPIError: If API request fails
        """
        if not self.service:
            raise GBPAPIError("Not authenticated. Call authenticate() first.")
        
        try:
            reply_data = {'comment': comment}
            return self.service.accounts().locations().reviews().updateReply(
                name=review_name,
                body=reply_data
            ).execute()
        except HttpError as e:
            self._handle_api_error(e)
    
    def get_performance_report(self, location_name: str, date_ranges: List[Dict[str, str]], 
                              metric_requests: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Get performance insights for a location
        
        Args:
            location_name: Location resource name
            date_ranges: List of date range dictionaries
            metric_requests: List of metric request dictionaries
            
        Returns:
            Performance report dictionary
            
        Raises:
            GBPAPIError: If API request fails
        """
        if not self.performance_service:
            raise GBPAPIError("Not authenticated. Call authenticate() first.")
        
        try:
            request_body = {
                'locationNames': [location_name],
                'basicRequest': {
                    'dateRanges': date_ranges,
                    'metricRequests': metric_requests
                }
            }
            
            return self.performance_service.locations().fetchMultiDailyMetricsTimeSeries(
                body=request_body
            ).execute()
        except HttpError as e:
            self._handle_api_error(e)