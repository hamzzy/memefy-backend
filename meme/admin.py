from django.contrib import admin

# Register your models here.
from meme.models import Meme,MemeCategories

admin.site.register(Meme)

admin.site.register(MemeCategories)