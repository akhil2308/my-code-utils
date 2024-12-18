import email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def read_eml(filename):
    with open(filename, 'r') as file:
        msg = email.message_from_file(file)
    return msg

def send_email(msg, sender_email, receiver_email, smtp_server, smtp_port, username, password):
    server = smtplib.SMTP_SSL(smtp_server, smtp_port)
    server.login(username, password)
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()

# Read the .eml file
eml_filename = 'example.eml'
email_message = read_eml(eml_filename)

# Extract necessary fields from the email
sender = email_message['To']
receiver = email_message['From']
subject = email_message['Subject']
body = email_message.get_payload()

# Define your SMTP server and credentials
smtp_server = 'smtp.example.com'
smtp_port = 465
username = ''
password = ''


# Send the email
send_email(email_message, sender, receiver, smtp_server, smtp_port, username, password)
