from django.db import models
from django.contrib.auth import get_user_model
from task.models import Task

User = get_user_model()


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    message = models.CharField(max_length=300, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
