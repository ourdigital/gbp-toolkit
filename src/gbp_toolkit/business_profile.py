"""
Business Profile management utilities and helper methods
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

from .client import GBPClient
from .exceptions import GBPAPIError


class BusinessProfileManager:
    """High-level business profile management operations"""
    
    def __init__(self, client: GBPClient):
        """
        Initialize business profile manager
        
        Args:
            client: Authenticated GBPClient instance
        """
        self.client = client
    
    def get_all_locations(self) -> List[Dict[str, Any]]:
        """
        Get all locations across all accessible accounts
        
        Returns:
            List of all location dictionaries with account info
        """
        all_locations = []
        accounts = self.client.list_accounts()
        
        for account in accounts:
            account_name = account['name']
            locations = self.client.list_locations(account_name)
            
            # Add account info to each location
            for location in locations:
                location['_account_name'] = account_name
                location['_account_type'] = account.get('type', 'UNKNOWN')
            
            all_locations.extend(locations)
        
        return all_locations
    
    def find_location_by_name(self, location_name: str) -> Optional[Dict[str, Any]]:
        """
        Find location by business name
        
        Args:
            location_name: Business name to search for
            
        Returns:
            Location dictionary if found, None otherwise
        """
        locations = self.get_all_locations()
        
        for location in locations:
            if location.get('locationName', '').lower() == location_name.lower():
                return location
        
        return None
    
    def update_business_hours(self, location_name: str, 
                             business_hours: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update business hours for a location
        
        Args:
            location_name: Location resource name
            business_hours: Business hours data structure
            
        Returns:
            Updated location dictionary
        """
        location_data = {'regularHours': business_hours}
        return self.client.update_location(
            location_name, 
            location_data, 
            update_mask='regularHours'
        )
    
    def update_contact_info(self, location_name: str, phone: Optional[str] = None, 
                           website: Optional[str] = None) -> Dict[str, Any]:
        """
        Update contact information for a location
        
        Args:
            location_name: Location resource name  
            phone: Primary phone number
            website: Website URL
            
        Returns:
            Updated location dictionary
        """
        location_data = {}
        update_fields = []
        
        if phone:
            location_data['primaryPhone'] = phone
            update_fields.append('primaryPhone')
        
        if website:
            location_data['websiteUri'] = website
            update_fields.append('websiteUri')
        
        if not location_data:
            raise GBPAPIError("No contact information provided to update")
        
        return self.client.update_location(
            location_name, 
            location_data, 
            update_mask=','.join(update_fields)
        )
    
    def get_recent_reviews(self, location_name: str, days: int = 30) -> List[Dict[str, Any]]:
        """
        Get recent reviews for a location
        
        Args:
            location_name: Location resource name
            days: Number of days to look back
            
        Returns:
            List of recent review dictionaries
        """
        all_reviews = self.client.list_reviews(location_name)
        cutoff_date = datetime.now() - timedelta(days=days)
        
        recent_reviews = []
        for review in all_reviews:
            create_time = review.get('createTime', '')
            if create_time:
                try:
                    review_date = datetime.fromisoformat(create_time.replace('Z', '+00:00'))
                    if review_date.replace(tzinfo=None) > cutoff_date:
                        recent_reviews.append(review)
                except ValueError:
                    continue
        
        return recent_reviews
    
    def get_unanswered_reviews(self, location_name: str) -> List[Dict[str, Any]]:
        """
        Get reviews that haven't been replied to
        
        Args:
            location_name: Location resource name
            
        Returns:
            List of unanswered review dictionaries
        """
        all_reviews = self.client.list_reviews(location_name)
        
        unanswered_reviews = []
        for review in all_reviews:
            if not review.get('reviewReply'):
                unanswered_reviews.append(review)
        
        return unanswered_reviews
    
    def bulk_reply_to_reviews(self, location_name: str, 
                             template: str = "Thank you for your review!") -> List[Dict[str, Any]]:
        """
        Reply to all unanswered reviews with a template message
        
        Args:
            location_name: Location resource name
            template: Reply template message
            
        Returns:
            List of reply result dictionaries
        """
        unanswered_reviews = self.get_unanswered_reviews(location_name)
        results = []
        
        for review in unanswered_reviews:
            try:
                result = self.client.reply_to_review(review['name'], template)
                results.append({
                    'review_name': review['name'], 
                    'status': 'success',
                    'result': result
                })
            except GBPAPIError as e:
                results.append({
                    'review_name': review['name'],
                    'status': 'error', 
                    'error': str(e)
                })
        
        return results
    
    def get_location_insights(self, location_name: str, days: int = 30) -> Dict[str, Any]:
        """
        Get performance insights for a location
        
        Args:
            location_name: Location resource name
            days: Number of days to analyze
            
        Returns:
            Insights dictionary with metrics
        """
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)
        
        date_ranges = [{
            'startDate': {'year': start_date.year, 'month': start_date.month, 'day': start_date.day},
            'endDate': {'year': end_date.year, 'month': end_date.month, 'day': end_date.day}
        }]
        
        metric_requests = [
            {'metric': 'ALL'},
        ]
        
        try:
            return self.client.get_performance_report(location_name, date_ranges, metric_requests)
        except GBPAPIError as e:
            return {'error': f"Unable to fetch insights: {str(e)}"}
    
    def validate_location_data(self, location_data: Dict[str, Any]) -> List[str]:
        """
        Validate location data for completeness and common issues
        
        Args:
            location_data: Location dictionary to validate
            
        Returns:
            List of validation issues found
        """
        issues = []
        
        # Check required fields
        required_fields = ['locationName', 'primaryCategory', 'address']
        for field in required_fields:
            if not location_data.get(field):
                issues.append(f"Missing required field: {field}")
        
        # Check address completeness
        address = location_data.get('address', {})
        address_fields = ['addressLines', 'locality', 'administrativeArea', 'postalCode']
        for field in address_fields:
            if not address.get(field):
                issues.append(f"Missing address field: {field}")
        
        # Check contact info
        if not location_data.get('primaryPhone'):
            issues.append("Missing primary phone number")
        
        # Check business hours
        if not location_data.get('regularHours'):
            issues.append("Missing business hours")
        
        return issues