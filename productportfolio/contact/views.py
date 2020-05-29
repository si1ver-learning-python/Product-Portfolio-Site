from django.shortcuts import render
from django.forms import *
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from . email_credentials import *

def contact(r):
    if r.method == "GET":
        return render(r, "contact/contact.html")
    elif r.method == "POST":
        email = r.POST["email"]
        name = r.POST["name"]
        detail = r.POST["detail"]
        detail = repr(detail).replace(r"\r\n", "<br>")

        message = MIMEMultipart("alternative")
        message["Subject"] = f"New Message From {email}"
        message["From"] = EMAIL
        message["To"] = EMAIL

        html = f"""
        <html>
        <body>
        <p><strong>Email:</strong>{email}</p>
        <p><strong>Name:</strong>{name}</p>
        <p><strong>Detail:</strong><br>{detail}</p>
        </body>
        </html>
        """

        mime = MIMEText(html, "html")
        message.attach(mime)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", PORT, context=context) as server:
            server.login(EMAIL, PASSWORD)
            server.sendmail(EMAIL, EMAIL, message.as_string())

        return render(r, "contact/complete.html")
