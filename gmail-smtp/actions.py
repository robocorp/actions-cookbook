from robocorp.actions import action

from RPA.Email.ImapSmtp import ImapSmtp


@action(is_consequential=True)
def send_email_via_gmail(subject: str, body: str, recipient: str) -> str:
    """
    Sends an email using Gmail SMTP with an App Password for authentication.

    :param subject: Email subject
    :param body: Email body content
    :param recipient: Recipient email address
    """
    # Initialize the email client with Gmail's SMTP settings
    mail = ImapSmtp(smtp_server="smtp.gmail.com", smtp_port=587)
    
    # SMTP authentication using your Gmail address and App Password
    # hardcoded for local testing only, move to env conf or secrets 
    gmail_address = ""
    app_password = ""

    mail.authorize(account=gmail_address, password=app_password)
    
    # Send an email
    mail.send_message(
        sender=gmail_address,
        recipients=[recipient],
        subject=subject,
        body=body,
    )

    return "email sent"

# Note: Ensure you have generated an App Password for your Gmail account. This method requires that 2-Step Verification is enabled for your Google account.
