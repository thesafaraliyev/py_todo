from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Task(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(max_length=500)
    deadline = models.DateTimeField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class TaskUser(models.Model):
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
        unique_together = ['user', 'task']
