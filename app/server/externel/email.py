import smtplib
import ssl
from email.message import EmailMessage


def send_email(new_payment):
    email_sender = 'lasnami.abdelkarim@gmail.com'
    email_password = 'wpzakzyzozwikhnj'
    email_receiver = 'lasnamiiwalid@gmail.com'

    subject = 'Nouvelle payement'
    body = """

    Nouveau versement: {new_payment}

    Traduction BOT.
    """

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())

