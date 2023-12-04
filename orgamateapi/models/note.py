from django.contrib.auth.models import User
from django.db import models

class Note(models.Model):
    item = models.ForeignKey("Item", on_delete=models.CASCADE, related_name='noteItemId')
    comment = models.CharField(max_length=155)
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='noteUserId')
