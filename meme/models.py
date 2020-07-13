from django.db import models
from user.models import User


# Create your models here.

class Meme(models.Model):
    """
    Meme image upload
    """

    title = models.CharField(max_length=200, null=False)
    file = models.FileField(blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Categories(models.Model):
    name = models.CharField(max_length=255)
    meme = models.ForeignKey(Meme, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
