from django.urls import path

from meme.views import MemeCatView, MemeView, MemeDelete, MemeAPIView, MemeSearch, MemeupdateView

urlpatterns  = [
    path('cat_meme',MemeCatView.as_view(),name="meme_cat"),
    path('meme',MemeView.as_view(),name='meme'),
    path('meme_delete/<uuid:id>/delete',MemeDelete.as_view()),
    path('meme_list', MemeAPIView.as_view()),
    path('meme_search/',MemeSearch.as_view(),name="meme-search"),
    path('meme_update/<uuid:id>/update', MemeupdateView.as_view(),name="meme-update")

]


