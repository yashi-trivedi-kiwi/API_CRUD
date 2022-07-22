from celery import shared_task

from django.core.mail import EmailMessage

from api_crud.settings import EMAIL_HOST_USER


@shared_task
def email_to_user(to_list):
    """
    To email send to advisor for generated password
    :return:
    """
    subject = "CELERY TEST MAIL"
    message = "Hi, This is celery test mail"
    email_from = EMAIL_HOST_USER
    msg = EmailMessage(subject, message, to=to_list, from_email=email_from)
    msg.content_subtype = 'html'
    msg.send()
    return "Mail has been sent from yashitrivedi802@gmail.com"
