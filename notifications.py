"""
notifications.py
-----------------
Handles notifications and optionally sending them via email.

Classes:
- notification: Encapsulates a message or alert.

Functions:
- send_email: Sends a notification message to a specified email address (optionally with a DataFrame attachment).
- main: Fetches bills and emails them.

Notes:
- Works with get_bills.py, which returns lists of notification objects.
- Email credentials must be stored in environment variables: EMAIL_USER, EMAIL_PASS.
"""

import smtplib
from email.message import EmailMessage
import pandas as pd
from io import StringIO
import os
from get_bills import get_bills  # Make sure get_bills.py is in the same directory
from notification_class import notification

def send_email(email_address: str, bill_notification: notification, df: pd.DataFrame = None) -> bool:
    """
    Sends an email containing the notification message and optionally attaches a DataFrame as CSV.

    Args:
        email_address (str): Recipient email address.
        bill_notification (notification): Notification object to send.
        df (pd.DataFrame, optional): DataFrame to attach as CSV.

    Returns:
        bool: True if the email was sent successfully, False otherwise.
    """
    sender_email = os.getenv("EMAIL_USER")
    sender_password = os.getenv("EMAIL_PASS")

    if not sender_email or not sender_password:
        print("Missing EMAIL_USER or EMAIL_PASS environment variables.")
        return False

    msg = EmailMessage()
    msg["Subject"] = "Notification"
    msg["From"] = sender_email
    msg["To"] = email_address
    msg.set_content(str(bill_notification))

    # Attach DataFrame if provided
    if df is not None and not df.empty:
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        msg.add_attachment(csv_buffer.getvalue(), subtype="csv", filename="bills.csv")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
        print(f"Email sent successfully to {email_address}")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False


def main():
    """
    Main function:
    - Fetches the latest bills using get_bills().
    - Loops through each notification and sends it via email.
    - Demonstrates attaching a DataFrame for email reports.
    """
    # Example date format: '11/04/2025'
    date_str = "9/10/2025"
    recipient = "lucasjamesnavarro@gmail.com"  # Replace with actual recipient email

    # Fetch notifications
    notifications_list = get_bills(date_str)

    # Send each notification individually (or batch via summary DataFrame)
    for n in notifications_list:
        send_email(recipient, n)  # Sends each message individually

if __name__ == "__main__":
    main()
