from django.contrib.auth.models import User
from django.db import models


class Task(models.Model):
    task_item = models.CharField(max_length=155)
    note = models.CharField(max_length=155)
    isComplete = models.BooleanField(default=False)
    date_added = models.DateField(auto_now_add=True)
    priority = models.ForeignKey("Priority", on_delete=models.CASCADE, related_name='priorityId')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todoUserId')