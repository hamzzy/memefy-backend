from django.shortcuts import render
from rest_framework import generics
# Create your views here.
from rest_framework.permissions import IsAuthenticated, AllowAny

from meme.Serializer import MemeCategory
from meme.models import MemeCategories


class MemeCatView(generics.ListCreateAPIView):
    permission_classes = (AllowAny,)
    queryset = MemeCategories.objects.all()
    serializer_class = MemeCategory



