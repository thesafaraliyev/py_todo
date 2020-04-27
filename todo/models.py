from django.db import models
from task.models import Task
from django.contrib.auth import get_user_model

User = get_user_model()


class Todo(models.Model):
    READ = 1
    COMMENT = 2

    ACCESS_TYPES = [
        (READ, 'Read only'),
        (COMMENT, 'Read and comment'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    access_type = models.PositiveSmallIntegerField(default=1, choices=ACCESS_TYPES)

    class Meta:
        unique_together = [['user', 'task']]
