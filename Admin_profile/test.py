import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# SMTP Server Configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SENDER_EMAIL = 'ebbysidiboubacar@gmail.com'
SENDER_PASSWORD = 'gypk flup iuxx yhkh'  # Use your Gmail password or app-specific password
RECIPIENT_EMAIL = 'ebbysidiboubacar@gmail.com'  # Replace with the recipient's email address

# Email Content
subject = 'Test Email'
body = 'This is a test email sent from Python script using Gmail SMTP.'

# Create the email message
message = MIMEMultipart()
message['From'] = SENDER_EMAIL
message['To'] = RECIPIENT_EMAIL
message['Subject'] = subject
message.attach(MIMEText(body, 'plain'))

# Send the email
try:
    # Set up the server and login
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()  # Secure the connection
    server.login(SENDER_EMAIL, SENDER_PASSWORD)

    # Send the email
    server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, message.as_string())
    print("Test email sent successfully!")

except Exception as e:
    print(f"Failed to send email: {str(e)}")

finally:
    server.quit()
