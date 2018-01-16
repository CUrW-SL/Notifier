# import the smtplib module. It should be included in Python by default
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import RECIPIENT_LIST
from config import EMAIL_SERVER_CONFIG


def send_email(run_source, checked_date, msg, recipient_list=RECIPIENT_LIST):
    try:
        # set up the SMTP server
        smtp_server = smtplib.SMTP(host=EMAIL_SERVER_CONFIG['host'], port=EMAIL_SERVER_CONFIG['port'])
        smtp_server.starttls()
        smtp_server.login(EMAIL_SERVER_CONFIG['user-name'], EMAIL_SERVER_CONFIG['password'])
        print("Successfully connected to the SMTP server at %s:%s !!"
              % (EMAIL_SERVER_CONFIG['host'], EMAIL_SERVER_CONFIG['port']))

        # create a multi-part email message
        email_message = MIMEMultipart()
        # setup the parameters of the message
        email_message['From'] = EMAIL_SERVER_CONFIG['user-name']
        email_message['To'] = ", ".join(recipient_list)
        email_message['Subject'] = "[%s][%s] Data Inconsistency!" % (run_source, checked_date)
        # add in the message body
        email_message.attach(MIMEText(msg, 'plain'))

        # send the message via the server set up earlier.
        smtp_server.send_message(email_message)
        print("Successfully sent the email notifications!!")
        smtp_server.quit()

    except Exception as ex:
        print("Error while sending email notifications: ", ex)
