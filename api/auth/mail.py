from flask_mail import Message
from flask import g
from flask import render_template
from common.config import ApiConfig
from flask_login import current_user


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    g.mail.send(msg)


def notification():
    send_email('Example mail.',
        ApiConfig.ADMINS[0],
        [current_user.email],
        render_template('index.html')
    )