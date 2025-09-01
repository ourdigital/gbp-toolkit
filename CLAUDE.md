# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Development Commands

```bash
# Install package in development mode
pip install -e .

# Install with development dependencies
pip install -e .[dev]

# Run tests
pytest

# Run tests with coverage
pytest --cov=gbp_toolkit

# Code formatting
black src/

# Type checking  
mypy src/

# Linting
flake8 src/

# Run examples (requires credentials.json)
cd examples && python basic_usage.py
cd examples && python review_management.py
cd examples && python location_management.py
```

## Architecture Overview

The toolkit follows a layered architecture for Google Business Profile API integration:

### Core Layers
- **GBPAuth** (`auth.py`) - OAuth2 authentication handler with automatic token refresh and credential storage
- **GBPClient** (`client.py`) - Low-level API client providing direct Google API access with error handling
- **BusinessProfileManager** (`business_profile.py`) - High-level business operations layer with convenience methods

### Authentication Flow
Authentication uses OAuth2 with local credential storage. The auth module handles the complete flow from initial authorization through token refresh. Tokens are stored in `token.json` and credentials are loaded from `credentials.json`.

### API Client Pattern
The client follows a consistent pattern:
1. All methods require prior authentication via `authenticate()`
2. HTTP errors are converted to `GBPAPIError` exceptions with status codes
3. Pagination is handled automatically for list operations
4. Resource names follow Google's hierarchical format (`accounts/123/locations/456`)

### Business Profile Manager
Provides domain-specific operations that may span multiple API calls:
- Cross-account location aggregation with account metadata injection
- Review analysis and bulk operations
- Location data validation against business requirements
- Performance insights integration with date range handling

### Error Handling Strategy
- **GBPError** - Base exception class
- **GBPAuthError** - Authentication failures (expired tokens, invalid credentials)
- **GBPAPIError** - API request failures with HTTP status codes and response bodies

## API Access Requirements

The Google Business Profile API is restricted and requires:
- Approved access application through Google
- Verified business profile active for 60+ days  
- OAuth2 credentials from Google Cloud Console
- Enabled APIs: Google My Business API and Business Profile Performance API

## Rate Limiting
- Location updates: 10 edits per minute per business profile (Google-enforced)
- Standard Google API quotas apply to all other operations

## Configuration Files
- `credentials.json` - OAuth2 client credentials (never commit)
- `token.json` - Access/refresh tokens (auto-generated, never commit)
- Both files should be in .gitignore for security