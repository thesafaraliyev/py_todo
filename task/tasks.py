from __future__ import absolute_import, unicode_literals

from celery import shared_task

from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_task_notify_mail(task_title, task_author, receiver):
    subject = f'New attached task #{task_title}'
    message = f'{task_author} attached new task to you.'
    send_mail(subject, message, settings.EMAIL_HOST_USER, [receiver])
