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
- `.env` - Environment variables for configuration (never commit)
- Both files should be in .gitignore for security

## Development Phases

### Phase 1: Core Toolkit Foundation ✅ COMPLETE
**Status**: Released in initial commit (v0.1.0)

**Completed Features**:
- Modular Python package architecture
- OAuth2 authentication with environment variable support
- Complete GBP API client with comprehensive error handling
- Business profile management utilities
- Review management and bulk operations
- Performance insights integration
- Location validation and CRUD operations
- Security-first credential protection
- Comprehensive documentation and examples

### Phase 2: Enterprise Features 🚀 IN PLANNING

#### Priority 1: CLI Interface (v0.2.0)
**Target**: User-friendly command-line interface to make operations accessible

**Implementation Notes**:
- Use Click or Typer for CLI framework
- Commands should follow pattern: `gbp <category> <action> [options]`
- Add to pyproject.toml console_scripts entry point
- Include progress bars for long operations
- Support --json output for automation

#### Priority 2: Enhanced Authentication (v0.2.0)
**Target**: Production-ready authentication management

**Implementation Notes**:
- Interactive setup wizard with validation
- Multiple profile support (personal, work, client-specific)
- Service account integration for server environments
- Token health monitoring and auto-refresh
- Keyring integration for secure storage

#### Priority 3: API Testing & Monitoring (v0.3.0)
**Target**: Robust connection testing and quota monitoring

**Implementation Notes**:
- Health check endpoints with retry logic
- Quota usage tracking with warnings
- Performance benchmarking with metrics collection
- Test suite integration with pytest
- CI/CD compatibility for automated testing

#### Priority 4: Google Maps URI Audit (v0.4.0)
**Target**: Automated location verification from Maps URLs

**Implementation Notes**:
- URL parser for Google Maps share links
- Places API integration for location verification
- Diff engine for comparing GBP vs Maps data
- Report generation with actionable recommendations
- Batch processing for multiple locations

## Development Guidelines for Phase 2

### CLI Implementation
- Place CLI commands in `src/gbp_toolkit/cli/`
- Use Click for command framework
- Implement `--help` for all commands
- Add progress indicators for long operations
- Support both interactive and automation modes

### Testing Strategy
- Add pytest fixtures for API mocking
- Create integration tests for CLI commands
- Mock external API calls in unit tests
- Add test data fixtures for different scenarios

### Google Maps Integration
- Use Google Places API for location data
- Parse Maps URLs with regex patterns
- Handle different Maps URL formats (short links, full URLs)
- Implement rate limiting for Maps API calls

### Authentication Enhancement
- Use keyring library for secure credential storage
- Support multiple credential profiles
- Add credential validation before API calls
- Implement service account authentication flow