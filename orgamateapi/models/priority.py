from django.db import models

class Priority(models.Model):
    label = models.CharField(max_length=20)