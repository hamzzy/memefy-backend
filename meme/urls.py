from django.urls import path

from meme.views import MemeCatView

urlpatterns=[
    path('create_cat_meme/',MemeCatView.as_view(),name="meme_cat")


]