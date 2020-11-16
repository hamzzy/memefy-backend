from django.db import models
from cloudinary.models import CloudinaryField
from authentication.models import CustomUser
import uuid


# Create your models here.
class MemeCategories(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=250, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Meme(models.Model):
    """
    Meme image upload
    """

    type = [
        ('Image'),
        ('Video')
    ]
    IMAGE = 'image'
    VIDEO = 'video'
    STATUS = [
        (IMAGE, 'image'),
        (VIDEO, 'video'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, null=False)
    file = CloudinaryField('memefy', default='')
    fileURL = models.CharField(max_length=100, verbose_name='File URL',default='')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    meme_type = models.CharField(max_length=32, choices=STATUS, default='image')
    meme_cat = models.ForeignKey(MemeCategories, on_delete=models.CASCADE, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.title
