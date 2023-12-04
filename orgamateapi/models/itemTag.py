from django.db import models

class ItemTag(models.Model):
    item = models.ForeignKey("Item", on_delete=models.CASCADE, related_name="item_tags" )
    tag = models.ForeignKey("Tag", on_delete=models.CASCADE, related_name="item_tags")
