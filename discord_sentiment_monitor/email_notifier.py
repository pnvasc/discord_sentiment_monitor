import smtplib
from email.mime.text import MIMEText
from .database import Session, Message
from sqlalchemy import desc

def check_sentiment_and_notify(session, threshold, manager_email):
    recent_messages = session.query(Message).order_by(Message.timestamp.desc()).limit(100).all()
    if not recent_messages:
        print("No recent messages found.")
        return
    avg_sentiment = sum(msg.sentiment_score for msg in recent_messages) / len(recent_messages)

    if avg_sentiment < threshold:
        send_email(email_address, "Negative Sentiment Alert", f"Average sentiment of last 10 messages: {avg_sentiment}")

    session.close()

def send_email(to_address, subject, body):
    # Implementation depends on your email provider
    from_address = "your_email@gmail.com"
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_address
    msg['To'] = to_address

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_address, "your_password")
    server.send_message(msg)
    server.quit()