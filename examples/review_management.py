#!/usr/bin/env python3
"""
Example for managing reviews using GBP Toolkit
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
    
    # Get first location for demo
    locations = manager.get_all_locations()
    if not locations:
        print("No locations found!")
        return
    
    location = locations[0]
    location_name = location['name']
    business_name = location.get('locationName', 'Unknown Business')
    
    print(f"Managing reviews for: {business_name}")
    print("=" * 50)
    
    # Get all reviews
    print("\n1. Fetching all reviews...")
    all_reviews = client.list_reviews(location_name)
    print(f"Total reviews: {len(all_reviews)}")
    
    # Analyze reviews
    ratings = []
    replied_count = 0
    
    for review in all_reviews:
        if 'starRating' in review:
            ratings.append(int(review['starRating']))
        if review.get('reviewReply'):
            replied_count += 1
    
    if ratings:
        avg_rating = sum(ratings) / len(ratings)
        print(f"Average rating: {avg_rating:.1f}/5")
        print(f"Reviews replied to: {replied_count}/{len(all_reviews)}")
    
    # Show recent reviews
    print("\n2. Recent reviews (last 30 days):")
    recent_reviews = manager.get_recent_reviews(location_name, days=30)
    
    for i, review in enumerate(recent_reviews[:5], 1):
        rating = review.get('starRating', 'N/A')
        reviewer = review.get('reviewer', {}).get('displayName', 'Anonymous')
        comment = review.get('comment', 'No comment')
        create_time = review.get('createTime', 'Unknown date')
        
        print(f"\n  Review {i}:")
        print(f"    Reviewer: {reviewer}")
        print(f"    Rating: {rating}/5")
        print(f"    Date: {create_time}")
        print(f"    Comment: {comment[:200]}{'...' if len(comment) > 200 else ''}")
        
        if review.get('reviewReply'):
            reply = review['reviewReply']
            print(f"    Reply: {reply.get('comment', 'No reply text')[:100]}...")
        else:
            print("    Reply: Not replied")
    
    # Find unanswered reviews
    print("\n3. Unanswered reviews:")
    unanswered = manager.get_unanswered_reviews(location_name)
    print(f"Found {len(unanswered)} unanswered reviews")
    
    if unanswered:
        print("\nFirst few unanswered reviews:")
        for i, review in enumerate(unanswered[:3], 1):
            rating = review.get('starRating', 'N/A')
            reviewer = review.get('reviewer', {}).get('displayName', 'Anonymous')
            comment = review.get('comment', 'No comment')
            
            print(f"\n  Unanswered Review {i}:")
            print(f"    Reviewer: {reviewer}")
            print(f"    Rating: {rating}/5") 
            print(f"    Comment: {comment[:150]}{'...' if len(comment) > 150 else ''}")
    
    # Demo: Reply to a specific review (commented out for safety)
    print("\n4. Reply to review example (commented out):")
    print("""
    # To reply to a specific review:
    # review_name = "accounts/123/locations/456/reviews/789"
    # reply_text = "Thank you for your feedback! We appreciate your business."
    # 
    # try:
    #     result = client.reply_to_review(review_name, reply_text)
    #     print("Reply posted successfully!")
    # except Exception as e:
    #     print(f"Failed to post reply: {e}")
    """)
    
    # Demo: Bulk reply (commented out for safety)
    print("\n5. Bulk reply example (commented out):")
    print("""
    # To reply to all unanswered reviews with a template:
    # template = "Thank you for taking the time to review us! Your feedback is valuable."
    # 
    # results = manager.bulk_reply_to_reviews(location_name, template)
    # 
    # for result in results:
    #     if result['status'] == 'success':
    #         print(f"Successfully replied to {result['review_name']}")
    #     else:
    #         print(f"Failed to reply to {result['review_name']}: {result['error']}")
    """)

if __name__ == "__main__":
    main()