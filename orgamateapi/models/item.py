from django.contrib.auth.models import User
from django.db import models

class Item(models.Model):
    image = models.CharField(max_length=200)
    name = models.CharField(max_length=155)
    description = models.CharField(max_length=155)
    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name='itemCategoryId')
    location = models.ForeignKey("Location", on_delete=models.CASCADE, related_name='itemLocationId')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='itemUserId')
    tags = models.ManyToManyField(
        "Tag",
        through="ItemTag",
        related_name="itemTags"
    )