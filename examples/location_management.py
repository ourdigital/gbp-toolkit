#!/usr/bin/env python3
"""
Example for managing location information using GBP Toolkit
"""

import os
from dotenv import load_dotenv
from gbp_toolkit import GBPClient, BusinessProfileManager

# Load environment variables
load_dotenv()

def main():
    # Initialize and authenticate
    client = GBPClient()
    client.authenticate()
    
    manager = BusinessProfileManager(client)
    
    # Get all locations
    print("Fetching all locations...")
    locations = manager.get_all_locations()
    
    if not locations:
        print("No locations found!")
        return
    
    print(f"Found {len(locations)} location(s)")
    print("=" * 50)
    
    # Display location summary
    for i, location in enumerate(locations, 1):
        name = location.get('locationName', 'Unknown')
        account = location.get('_account_name', 'Unknown')
        address = location.get('address', {})
        address_line = address.get('addressLines', ['N/A'])[0] if address.get('addressLines') else 'N/A'
        
        print(f"\n{i}. {name}")
        print(f"   Account: {account}")
        print(f"   Address: {address_line}")
        print(f"   Resource: {location['name']}")
    
    # Work with first location for detailed examples
    if locations:
        location = locations[0]
        location_name = location['name']
        business_name = location.get('locationName', 'Unknown Business')
        
        print(f"\n\nDetailed analysis for: {business_name}")
        print("=" * 50)
        
        # Get full location details
        print("\n1. Location Details:")
        details = client.get_location(location_name)
        
        # Basic info
        print(f"   Name: {details.get('locationName', 'N/A')}")
        print(f"   Primary Category: {details.get('primaryCategory', {}).get('displayName', 'N/A')}")
        
        # Address
        address = details.get('address', {})
        if address:
            lines = address.get('addressLines', [])
            locality = address.get('locality', '')
            admin_area = address.get('administrativeArea', '')
            postal_code = address.get('postalCode', '')
            
            full_address = ', '.join(filter(None, [
                ' '.join(lines) if lines else '',
                locality,
                admin_area,
                postal_code
            ]))
            print(f"   Address: {full_address}")
        
        # Contact info
        print(f"   Phone: {details.get('primaryPhone', 'N/A')}")
        print(f"   Website: {details.get('websiteUri', 'N/A')}")
        
        # Business hours
        regular_hours = details.get('regularHours')
        if regular_hours:
            print("\n   Business Hours:")
            periods = regular_hours.get('periods', [])
            for period in periods:
                day = period.get('openDay', 'Unknown')
                open_time = period.get('openTime', {})
                close_time = period.get('closeTime', {})
                
                open_str = f"{open_time.get('hours', 0):02d}:{open_time.get('minutes', 0):02d}" if open_time else 'Closed'
                close_str = f"{close_time.get('hours', 0):02d}:{close_time.get('minutes', 0):02d}" if close_time else 'Closed'
                
                if open_time and close_time:
                    print(f"     {day}: {open_str} - {close_str}")
                else:
                    print(f"     {day}: Closed")
        
        # Validation
        print("\n2. Location Validation:")
        issues = manager.validate_location_data(details)
        if issues:
            print("   Issues found:")
            for issue in issues:
                print(f"     ⚠️  {issue}")
        else:
            print("   ✅ Location data is complete")
        
        # Performance insights
        print("\n3. Performance Insights (last 30 days):")
        insights = manager.get_location_insights(location_name, days=30)
        if 'error' in insights:
            print(f"   ❌ {insights['error']}")
        else:
            print("   ✅ Insights retrieved successfully")
            # Note: Actual insight data structure depends on API response
            print("   (Detailed insights would be processed here)")
        
        # Example updates (commented out for safety)
        print("\n4. Example Updates (commented out for safety):")
        print("""
        # Update contact information:
        # result = manager.update_contact_info(
        #     location_name,
        #     phone="+1-555-123-4567",
        #     website="https://example.com"
        # )
        
        # Update business hours:
        # business_hours = {
        #     "periods": [
        #         {
        #             "openDay": "MONDAY",
        #             "openTime": {"hours": 9, "minutes": 0},
        #             "closeDay": "MONDAY", 
        #             "closeTime": {"hours": 17, "minutes": 0}
        #         },
        #         # ... more days
        #     ]
        # }
        # result = manager.update_business_hours(location_name, business_hours)
        """)
    
    # Search example
    print("\n5. Location Search Example:")
    print("Searching for location by name (case-insensitive)...")
    
    if locations:
        # Use first location's name for demo
        search_name = locations[0].get('locationName', '')
        if search_name:
            found_location = manager.find_location_by_name(search_name)
            if found_location:
                print(f"   ✅ Found: {found_location.get('locationName')}")
            else:
                print(f"   ❌ Not found: {search_name}")

if __name__ == "__main__":
    main()