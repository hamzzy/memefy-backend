from django.db import models

from MemeApp import settings
from authentication.models import CustomUser
import uuid


# Create your models here.

class Meme(models.Model):

    """
    Meme image upload
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, null=False)
    file = models.FileField(blank=False, null=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Categories(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=250, null=True, blank=True)
    meme = models.ForeignKey(Meme, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
