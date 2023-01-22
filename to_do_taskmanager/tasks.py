from django.core.mail import send_mail
from celery import shared_task
from .views import Task


@shared_task
def send_task_email(task_id):
    task = Task.objects.get(id=task_id)
    send_mail(
        'New task assigned to you',
        'You have been assigned a new task: ' + task.title,
        'from@example.com',
        [task.assigned_to.email],
        fail_silently=False,
    )
