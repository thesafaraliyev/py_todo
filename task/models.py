from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(max_length=500)
    deadline = models.DateTimeField()

    def __str__(self):
        return self.title
