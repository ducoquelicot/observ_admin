from flask_mail import Message
from app import observ, mail
from flask import render_template
from threading import Thread
from jinja2 import Template 
import pathlib

def send_async_email(observ, msg):
    with observ.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
#     with observ.app_context():
#         msg.body = text_body
#         msg.html = html_body
#         mail.send(msg)
    Thread(target=send_async_email, args=(observ, msg)).start()

def send_job_mail(subject, sender, recipients, text_body, html_body):
        msg = Message(subject, sender=sender, recipients=recipients)
        with observ.app_context():
                msg.body = text_body
                msg.html = html_body
                mail.send(msg)

def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('[observ] reset your password',
                sender=observ.config['ADMINS'][0],
                recipients=[user.email],
                text_body=render_template('email/reset_password.txt',
                                            user=user, token=token),
                html_body=render_template('email/reset_password.html',
                                            user=user, token=token)
            )

def send_sub_email(user, subscription):
        send_email('[observ] Your new subscription',
        sender=observ.config['ADMINS'][0],
        recipients=[user.email],
        text_body=render_template('email/send_sub.txt',
                                user=user, subscription=subscription),
        html_body=render_template('email/send_sub.html',
                                user=user, subscription=subscription)
        )

def send_results_email(user, subscription, results):
        text_template = Template(open(pathlib.Path(__file__).parent / 'templates/email/send_results.txt').read())
        html_template = Template(open(pathlib.Path(__file__).parent / 'templates/email/send_results.html').read())

        send_job_mail('[observ] New results for your subscription',
        sender=observ.config['ADMINS'][0],
        recipients=[user.email],
        text_body=text_template.render(user=user, subscription=subscription, results=results),
        html_body=html_template.render(user=user, subscription=subscription, results=results)
        )