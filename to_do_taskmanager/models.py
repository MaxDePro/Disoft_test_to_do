from django.db import models
from django.contrib.auth.models import User


# class Image(models.Model):
#     image = models.ImageField('Image', upload_to='tasks/')


class Task(models.Model):
    STATUS_CHOICES = (
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )
    title = models.CharField('Title', max_length=255)
    task_text = models.TextField('Task Text')
    status = models.CharField('Status', max_length=11, choices=STATUS_CHOICES)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_tasks', default=User)
    assigned_to = models.ManyToManyField(User, related_name='assigned_tasks')
    created_at = models.DateTimeField('Created at', auto_now_add=True)
    edited_at = models.DateTimeField('Edited at', auto_now=True)
    images = models.ImageField(upload_to='tasks/', blank=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text
