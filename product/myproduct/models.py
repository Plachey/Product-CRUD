import uuid

from django.db import models


class Products(models.Model):
    uuid = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='product/')
    rotate_duration = models.FloatField(blank=True, null=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(blank=True, null=True)
