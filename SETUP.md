# Google Business Profile API Setup Guide

This guide walks you through setting up access to the Google Business Profile API for the GBP Toolkit.

## Prerequisites

1. **Google Business Profile**: You must have a verified Google Business Profile that has been active for 60+ days
2. **Google Cloud Project**: Access to Google Cloud Console to create projects and enable APIs
3. **API Access Application**: The GBP API is restricted and requires approved access

## Step 1: Apply for GBP API Access

⚠️ **IMPORTANT**: The Google Business Profile API is not publicly available. You must apply for access first.

### Requirements for Application:
- Verified Google Business Profile active for 60+ days
- Clear business use case for API access
- Compliance with Google's Business Profile API policies

### How to Apply:
1. Visit the [Google Business Profile API documentation](https://developers.google.com/my-business)
2. Look for the "Request Access" or "Apply for Access" section
3. Fill out the application form with:
   - Business information
   - Use case description
   - Expected API usage patterns
4. Wait for Google's approval (can take several weeks)

## Step 2: Set Up Google Cloud Project

Once you have API access approval:

1. **Create a Project**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one
   - Note your Project ID

2. **Enable Required APIs**:
   - Navigate to "APIs & Services" > "Library"
   - Search for and enable:
     - "Google My Business API"
     - "Business Profile Performance API"

3. **Create OAuth2 Credentials**:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth 2.0 Client IDs"
   - Choose "Desktop application" as the application type
   - Add authorized redirect URIs:
     - `http://localhost:8080/callback`
     - `urn:ietf:wg:oauth:2.0:oob` (for fallback)
   - Download the credentials JSON file

## Step 3: Configure Your Local Environment

1. **Copy the credentials file**:
   ```bash
   # Copy your downloaded credentials file
   cp ~/Downloads/client_secret_*.json credentials.json
   ```

2. **Set up environment variables**:
   ```bash
   # Copy the template
   cp .env.example .env
   
   # Edit .env with your actual values
   nano .env
   ```

3. **Update .env file**:
   ```env
   # Required settings
   GBP_CREDENTIALS_FILE=credentials.json
   GBP_TOKEN_FILE=token.json
   GBP_REDIRECT_URI=http://localhost:8080/callback
   
   # Your Google Cloud Project ID
   GOOGLE_CLOUD_PROJECT_ID=your-actual-project-id
   
   # Optional: Development settings
   DEBUG_MODE=true
   LOG_LEVEL=DEBUG
   ```

## Step 4: Install and Test

1. **Install the toolkit**:
   ```bash
   pip install -e .[dev]
   ```

2. **Test authentication**:
   ```bash
   cd examples
   python basic_usage.py
   ```

3. **Follow OAuth flow**:
   - The script will open a browser window
   - Sign in with your Google account
   - Grant permissions to your application
   - Copy the authorization code back to the terminal

## Step 5: Verify Setup

After successful authentication, you should have:
- `credentials.json` - OAuth2 client credentials
- `token.json` - Access/refresh tokens (auto-generated)
- `.env` - Environment configuration

Test that everything works:
```python
from gbp_toolkit import GBPClient

client = GBPClient()
client.authenticate()

# This should list your accounts without errors
accounts = client.list_accounts()
print(f"Found {len(accounts)} account(s)")
```

## Common Issues and Solutions

### 1. "API not enabled" Error
**Solution**: Make sure you've enabled both required APIs in Google Cloud Console:
- Google My Business API
- Business Profile Performance API

### 2. "Access denied" or "Forbidden" Error
**Solution**: You likely don't have approved access to the GBP API. You must apply and wait for approval.

### 3. "Invalid redirect URI" Error
**Solution**: Check that your OAuth2 client has the correct redirect URIs:
- `http://localhost:8080/callback`
- `urn:ietf:wg:oauth:2.0:oob`

### 4. "Credentials file not found"
**Solution**: Make sure `credentials.json` is in your working directory or update the path in `.env`:
```env
GBP_CREDENTIALS_FILE=/path/to/your/credentials.json
```

### 5. Token Refresh Issues
**Solution**: Delete `token.json` and re-authenticate:
```bash
rm token.json
python examples/basic_usage.py
```

## Security Best Practices

1. **Never commit sensitive files**:
   - `credentials.json`
   - `token.json` 
   - `.env`

2. **Use service accounts for production**:
   - For server applications, consider using service account credentials
   - Store credentials securely (e.g., Google Secret Manager, environment variables)

3. **Rotate credentials regularly**:
   - Regenerate OAuth2 credentials periodically
   - Revoke old credentials when no longer needed

4. **Limit scope**:
   - Only request necessary OAuth scopes
   - Currently using: `https://www.googleapis.com/auth/business.manage`

## Getting Help

If you encounter issues:

1. **Check Google's documentation**: [Google Business Profile API docs](https://developers.google.com/my-business)
2. **Verify your API access status**: Contact Google if your application status is unclear
3. **Review quota limits**: Check your API usage in Google Cloud Console
4. **Test with Google's API Explorer**: Use the online API explorer to test requests

## Rate Limits

Be aware of these limits:
- **Location updates**: Maximum 10 edits per minute per Google Business Profile
- **API requests**: Standard Google API quotas apply
- **Daily limits**: Check your specific quota in Google Cloud Console

## Next Steps

Once setup is complete:
1. Explore the examples in the `examples/` directory
2. Review the API documentation in `README.md`
3. Start building your GBP management application!