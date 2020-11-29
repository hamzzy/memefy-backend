from django.shortcuts import get_object_or_404
from rest_framework import serializers

from authentication.Serializer import CustomUserSerializer
from meme.models import MemeCategories, Meme
import django_filters


class MemeCategory(serializers.ModelSerializer):
    '''
    authentication serilizer
    '''

    class Meta:
        model = MemeCategories
        fields = ['id', 'name', 'slug']
        read_only_fields = ('id',)


class MemeSerializer(serializers.ModelSerializer):
    fileURL = serializers.CharField(required=False)
    user = CustomUserSerializer(required=False, )

    class Meta:
        model = Meme
        fields = ('id', 'title', 'fileURL', 'user', 'meme_type', 'meme_cat')


class MemeFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Meme
        fields = ['title']
