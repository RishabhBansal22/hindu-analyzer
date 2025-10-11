# GitHub Actions Setup for Automated Email Reports

This document explains how to set up the automated email reporting system using GitHub Actions.

## Overview

The GitHub Actions workflow (`report.yml`) automatically:
1. Scrapes The Hindu editorial articles
2. Analyzes them using Gemini AI
3. Generates a PDF report
4. Sends the report via email

## Prerequisites

### 1. Gmail App Password Setup

Since this workflow uses Gmail SMTP, you need to set up an App Password:

1. Go to your Google Account settings
2. Navigate to Security → 2-Step Verification (enable if not already enabled)
3. Go to App passwords
4. Create a new app password for "Mail"
5. Save this password - you'll use it as `GMAIL_APP_PASS` secret

### 2. Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Create a new API key
3. Save this key - you'll use it as `GEMINI_API_KEY` secret

## Required GitHub Secrets

Set up the following secrets in your GitHub repository:

### Navigation: Repository → Settings → Secrets and variables → Actions → New repository secret

| Secret Name | Description | Example |
|-------------|-------------|---------|
| `SENDER_MAIL` | Gmail address that will send the emails | `your.email@gmail.com` |
| `RECEIVER_MAIL` | Email address that will receive the reports | `recipient@example.com` |
| `GMAIL_APP_PASS` | Gmail App Password (16 characters) | `abcd efgh ijkl mnop` |
| `GEMINI_API_KEY` | Google Gemini API key | `AIzaSyC...` |

## Workflow Configuration

### Automatic Schedule
- **Default**: Runs daily at 9:00 AM IST (3:30 AM UTC)
- **Customization**: Edit the cron expression in `report.yml`:
  ```yaml
  schedule:
    - cron: '30 3 * * *'  # Change this time
  ```

### Manual Trigger
You can manually trigger the workflow with custom parameters:

1. Go to Actions → Automated Email Report → Run workflow
2. Optional parameters:
   - **Number of articles**: How many articles to analyze (default: 2)
   - **Recipient email**: Override the default recipient

## Workflow Features

### ✅ Success Features
- Automatically analyzes Hindu editorials
- Generates detailed PDF reports
- Sends emails with PDF attachments
- Caches dependencies for faster runs
- Supports manual triggers with parameters

### 🛡️ Error Handling
- Validates all required secrets before running
- Falls back to simple PDF if detailed PDF fails
- Sends failure notifications if workflow fails
- Uploads logs and PDFs as artifacts for debugging
- Graceful error handling and logging

### 📊 Monitoring
- Check workflow status in GitHub Actions tab
- View detailed logs for each step
- Download artifacts if workflow fails
- Receive email notifications on failures

## Timezone Considerations

The default schedule runs at 9:00 AM IST (3:30 AM UTC). To adjust for other timezones:

| Timezone | Cron Expression | Description |
|----------|----------------|-------------|
| IST (UTC+5:30) | `30 3 * * *` | 9:00 AM IST (current setting) |
| UTC | `0 9 * * *` | 9:00 AM UTC |
| EST (UTC-5) | `0 14 * * *` | 9:00 AM EST |
| PST (UTC-8) | `0 17 * * *` | 9:00 AM PST |

## Testing the Setup

### 1. Manual Test
1. Go to Actions → Automated Email Report
2. Click "Run workflow"
3. Set "Number of articles" to 1 (for faster testing)
4. Monitor the workflow execution

### 2. Check Logs
- View each step's output in the Actions tab
- Look for success messages like "✅ Email sent successfully!"
- Check for any error messages or warnings

### 3. Verify Email
- Check the recipient email inbox
- Verify PDF attachment is present and readable
- Ensure email content looks correct

## Troubleshooting

### Common Issues

1. **Secret Access Errors**
   - Verify all required secrets are set correctly
   - Check secret names match exactly (case-sensitive)

2. **Gmail Authentication Errors**
   - Ensure 2-Step Verification is enabled
   - Verify App Password is correct (16 characters with spaces)
   - Make sure Gmail account allows less secure app access

3. **Gemini API Errors**
   - Verify API key is valid and active
   - Check API quota limits
   - Ensure Gemini API is enabled in Google Cloud Console

4. **PDF Generation Errors**
   - Check logs for detailed error messages
   - Workflow will attempt simple PDF if detailed PDF fails
   - Artifacts will be uploaded for debugging

### Debug Steps

1. **Check Workflow Logs**: Actions tab → Latest run → Click on failed step
2. **Download Artifacts**: Failed runs upload logs and PDFs for analysis
3. **Test Locally**: Run the workflow script locally with same environment variables
4. **Manual Email Test**: Test email sending separately from analysis

## Security Best Practices

- ✅ Never commit API keys or passwords to code
- ✅ Use GitHub Secrets for all sensitive data
- ✅ Regularly rotate API keys and app passwords
- ✅ Monitor workflow logs for any exposed sensitive data
- ✅ Use App Passwords instead of main Gmail password

## Customization Options

### Modify Analysis Parameters
Edit the workflow file to change:
- Number of articles analyzed
- Analysis frequency (cron schedule)
- PDF report format
- Email content and subject

### Add More Recipients
Modify the email sending logic to support multiple recipients:
```python
msg["To"] = "recipient1@example.com, recipient2@example.com"
```

### Custom PDF Styling
Modify `main.py` functions:
- `save_results_to_pdf()` - Detailed PDF format
- `save_simple_pdf()` - Simple PDF format

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review workflow logs in GitHub Actions
3. Test components individually (API access, email sending, PDF generation)
4. Ensure all prerequisites are met