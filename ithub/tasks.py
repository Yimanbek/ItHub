from account.send_email import  send_confirmation_email , send_confirmation_password,send_respond_data,send_comment_notification
from .celery import celery_app

@celery_app.task()
def send_confirmation_email_task(email , code):
    send_confirmation_email(email,code)


@celery_app.task()
def send_confirmation_password_task(email , code):
    send_confirmation_password(email,code)

@celery_app.task()
def send_comment_notification_tasks(post_author,content,email_from):
    send_comment_notification(post_author,content,email_from)

@celery_app.task()
def send_respond_data_task(full_name, characteristics, phone_number, email, short_intro, additional_info, owner_email):
    send_respond_data(full_name, characteristics, phone_number, email, short_intro, additional_info, owner_email)