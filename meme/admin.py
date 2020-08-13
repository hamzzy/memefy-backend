from django.contrib import admin
admin.site.site_header = "MEMEFY Admin"
admin.site.site_title = "Admin Panel to Memefy"
admin.site.index_title = "welcome to memefy admin board"
# Register your models here.
from meme.models import Meme,MemeCategories

admin.site.register(Meme)

admin.site.register(MemeCategories)