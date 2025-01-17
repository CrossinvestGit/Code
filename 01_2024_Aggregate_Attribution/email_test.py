"""
Send an email with an attached Excel file.
"""
import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email_with_excel(sender_email, receiver_email, subject, body, excel_file_path):
    """
    Sends an email with an attached Excel file.

    Args:
        sender_email (str): The email address of the sender.
        receiver_email (str): The email address of the receiver.
        subject (str): The subject of the email.
        body (str): The body of the email.
        excel_file_path (str): The file path of the Excel file to be attached.

    Returns:
        None
    """
    # Create a multipart message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    # Add body to email
    message.attach(MIMEText(body, "plain"))
    # Open the file in binary
    with open(excel_file_path, "rb"):
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        # part.set_payload(attachment.read())
        part.set_payload(open(excel_file_path, "rb").read())

    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        "attachment",
        filename=os.path.basename(excel_file_path),
    )  # Only use the base filename

    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()

    # Log in to the email server
    smtp_server = "172.16.121.13"
    smtp_port = 25

    server = smtplib.SMTP(smtp_server, smtp_port)

    # Send email
    server.sendmail(sender_email, receiver_email, text)
    server.quit()


# Usage example


send_email_with_excel(
    sender_email="a.ramadani@crossinvest.ch",
    receiver_email="a.ramadani@crossinvest.ch",
    subject="Contribution",
    body="""
Please find attached the Excel file.

This mail was automatically generated. Please check the data before using it.
""",
    excel_file_path=(
        "Z:/14_Personal_Data/a.ramadani/Code/"
        "01_2024_Aggregate_Attribution/output/output_file.xlsx"
    ),
)
