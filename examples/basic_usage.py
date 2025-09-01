#!/usr/bin/env python3
"""
Basic usage example for GBP Toolkit
"""

import os
from dotenv import load_dotenv
from gbp_toolkit import GBPClient, BusinessProfileManager

# Load environment variables
load_dotenv()

def main():
    # Initialize client
    client = GBPClient()
    
    # Authenticate (credentials will be loaded from environment variables or defaults)
    print("Authenticating with Google Business Profile API...")
    print(f"Using credentials: {os.getenv('GBP_CREDENTIALS_FILE', 'credentials.json')}")
    print(f"Using token file: {os.getenv('GBP_TOKEN_FILE', 'token.json')}")
    
    client.authenticate()
    
    # Initialize business profile manager
    manager = BusinessProfileManager(client)
    
    # List all accounts
    print("\n=== Accounts ===")
    accounts = client.list_accounts()
    for account in accounts:
        print(f"Account: {account['name']} - {account.get('accountName', 'N/A')}")
    
    # Get all locations
    print("\n=== Locations ===")
    locations = manager.get_all_locations()
    for location in locations:
        name = location.get('locationName', 'N/A')
        account = location.get('_account_name', 'N/A')
        print(f"Location: {name} (Account: {account})")
    
    if locations:
        # Work with first location
        first_location = locations[0]
        location_name = first_location['name']
        business_name = first_location.get('locationName', 'Unknown')
        
        print(f"\n=== Working with: {business_name} ===")
        
        # Get location details
        location_details = client.get_location(location_name)
        print(f"Address: {location_details.get('address', {}).get('addressLines', ['N/A'])[0]}")
        print(f"Phone: {location_details.get('primaryPhone', 'N/A')}")
        print(f"Website: {location_details.get('websiteUri', 'N/A')}")
        
        # List recent reviews
        print("\n=== Recent Reviews (last 30 days) ===")
        recent_reviews = manager.get_recent_reviews(location_name, days=30)
        print(f"Found {len(recent_reviews)} recent reviews")
        
        for review in recent_reviews[:3]:  # Show first 3
            rating = review.get('starRating', 'N/A')
            comment = review.get('comment', 'No comment')[:100] + '...'
            print(f"Rating: {rating}/5 - {comment}")
        
        # Check for unanswered reviews
        print("\n=== Unanswered Reviews ===")
        unanswered = manager.get_unanswered_reviews(location_name)
        print(f"Found {len(unanswered)} unanswered reviews")
        
        # Get insights (if available)
        print("\n=== Location Insights ===")
        insights = manager.get_location_insights(location_name, days=30)
        if 'error' in insights:
            print(f"Insights not available: {insights['error']}")
        else:
            print("Insights retrieved successfully")
        
        # Validate location data
        print("\n=== Location Validation ===")
        issues = manager.validate_location_data(location_details)
        if issues:
            print("Validation issues found:")
            for issue in issues:
                print(f"  - {issue}")
        else:
            print("Location data is complete")

if __name__ == "__main__":
    main()