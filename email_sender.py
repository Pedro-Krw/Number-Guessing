import smtplib
from email.mime.text import MIMEText

def send_email(to_email):
    sender_email = "kibaxmandows@gmail.com"
    sender_pass = "jthn jlgy enmn ssnb"

    msg = MIMEText("Selamat! Kamu memenangkan game tebak angka!")
    msg['Subject'] = "Kemenangan Game"
    msg['From'] = sender_email
    msg['To'] = to_email

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, sender_pass)
            smtp.send_message(msg)
        print(f"[EMAIL SENT] ke {to_email}")
    except Exception as e:
        print(f"[EMAIL FAILED] {e}")
