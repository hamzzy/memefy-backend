from django.db import models

from MemeApp import settings
from MemeApp.storage_backends import PrivateMediaStorage, PublicMediaStorage
from authentication.models import CustomUser
import uuid


# Create your models here.
class MemeCategories(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.name


class Meme(models.Model):
    """
    Meme image upload
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, null=False)
    image= models.FileField(storage=PublicMediaStorage(),default='')
    video=models.FileField(storage=PublicMediaStorage(),default='')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    memecat = models.ForeignKey(MemeCategories, on_delete=models.CASCADE, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.title
