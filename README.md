# GBP Toolkit

A Python toolkit for managing Google Business Profile via the Google Business Profile APIs.

## Features

- **Authentication**: OAuth2 authentication flow with token management
- **Account Management**: List and manage Google Business Profile accounts
- **Location Management**: CRUD operations for business locations
- **Review Management**: List, analyze, and reply to customer reviews
- **Performance Insights**: Access business performance metrics
- **Bulk Operations**: Perform operations across multiple locations
- **Validation**: Validate location data completeness

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd gbp-toolkit

# Install the package
pip install -e .

# Or install with development dependencies
pip install -e .[dev]
```

## Prerequisites

1. **Google Cloud Project**: Create a project in the Google Cloud Console
2. **Enable APIs**: Enable the Google My Business API and Business Profile Performance API
3. **OAuth2 Credentials**: Create OAuth2 credentials and download the JSON file
4. **API Access**: Apply for Google Business Profile API access (restricted API)

### Getting API Access

The Google Business Profile API is not publicly available. You need to:

1. Have a verified Google Business Profile that's been active for 60+ days
2. Meet Google's criteria for API access
3. Apply through the official Google process
4. Wait for approval (this can take several weeks)

## Quick Start

```python
from gbp_toolkit import GBPClient, BusinessProfileManager

# Initialize client
client = GBPClient()

# Authenticate (requires credentials.json file)
client.authenticate(
    credentials_file='credentials.json',
    token_file='token.json'
)

# Initialize business profile manager for high-level operations
manager = BusinessProfileManager(client)

# List all locations
locations = manager.get_all_locations()
for location in locations:
    print(f"Business: {location.get('locationName')}")

# Get recent reviews for a location
if locations:
    location_name = locations[0]['name']
    recent_reviews = manager.get_recent_reviews(location_name, days=30)
    print(f"Recent reviews: {len(recent_reviews)}")
```

## Examples

The `examples/` directory contains detailed usage examples:

- `basic_usage.py` - Basic operations and data retrieval
- `review_management.py` - Managing customer reviews
- `location_management.py` - Location information management

Run examples:

```bash
cd examples
python basic_usage.py
python review_management.py
python location_management.py
```

## API Reference

### GBPClient

Core client for Google Business Profile API operations.

#### Methods

- `authenticate(credentials_file, token_file, redirect_uri)` - Authenticate with OAuth2
- `list_accounts()` - List all accessible accounts
- `get_account(account_name)` - Get specific account details
- `list_locations(account_name)` - List locations for an account
- `get_location(location_name)` - Get location details
- `update_location(location_name, location_data, update_mask)` - Update location
- `list_reviews(location_name)` - List reviews for a location
- `reply_to_review(review_name, comment)` - Reply to a review
- `get_performance_report(location_name, date_ranges, metric_requests)` - Get insights

### BusinessProfileManager

High-level business profile management operations.

#### Methods

- `get_all_locations()` - Get all locations across accounts
- `find_location_by_name(location_name)` - Find location by business name
- `update_business_hours(location_name, business_hours)` - Update operating hours
- `update_contact_info(location_name, phone, website)` - Update contact information
- `get_recent_reviews(location_name, days)` - Get reviews from last N days
- `get_unanswered_reviews(location_name)` - Get reviews without replies
- `bulk_reply_to_reviews(location_name, template)` - Reply to all unanswered reviews
- `get_location_insights(location_name, days)` - Get performance insights
- `validate_location_data(location_data)` - Validate location completeness

### GBPAuth

Authentication handler for OAuth2 flow.

#### Methods

- `authenticate(redirect_uri)` - Perform OAuth2 authentication
- `get_service(service_name, version)` - Get authenticated API service
- `revoke_credentials()` - Revoke stored credentials

## Configuration

### Credentials Setup

1. Download OAuth2 credentials JSON from Google Cloud Console
2. Save as `credentials.json` in your working directory
3. The toolkit will create `token.json` automatically after first authentication

### Environment Variables

You can set default paths using environment variables:

```bash
export GBP_CREDENTIALS_FILE="/path/to/credentials.json"
export GBP_TOKEN_FILE="/path/to/token.json"
```

## Rate Limits

- **Location Updates**: 10 edits per minute per Google Business Profile
- **API Requests**: Standard Google API quotas apply

## Error Handling

The toolkit provides custom exceptions:

- `GBPError` - Base exception
- `GBPAuthError` - Authentication failures
- `GBPAPIError` - API request/response errors

```python
from gbp_toolkit.exceptions import GBPAPIError

try:
    locations = client.list_locations(account_name)
except GBPAPIError as e:
    print(f"API Error: {e}")
    print(f"Status Code: {e.status_code}")
```

## Development

```bash
# Install development dependencies
pip install -e .[dev]

# Run tests
pytest

# Code formatting
black src/

# Type checking
mypy src/

# Linting
flake8 src/
```

## Security Notes

- Never commit `credentials.json` or `token.json` to version control
- Store credentials securely in production environments
- Use service accounts for server-to-server authentication when possible
- Regularly rotate OAuth2 tokens

## Limitations

- Requires approved access to Google Business Profile API
- Rate limits apply to all operations
- Some advanced features may require additional API permissions
- Performance insights availability depends on business type and data

## Support

- [Google Business Profile API Documentation](https://developers.google.com/my-business)
- [Google Business Profile Help Center](https://support.google.com/business/)

## License

MIT License - see LICENSE file for details.