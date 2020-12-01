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
    user = CustomUserSerializer(required=True )

    class Meta:
        model = Meme
        fields = ('id', 'title', 'fileURL', 'user', 'meme_type', 'meme_cat')


        # def update(self, instance, validated_data):
        #
        #     return instance

# class MemeUpdateSerializer(serializers.Serializer):
#     fileURL = serializers.CharField(required=False)
#     title = serializers.CharField(max_length=255,write_only=True)
#     title = serializers.CharField(max_length=255,write_only=True)
#     user = serializers.HiddenField(default=serializers.CurrentUserDefault())
#
#     def __init__(self, *args, **kwargs):
#         super(MemeUpdateSerializer, self).__init__(*args, **kwargs)
#         self.fields["fileURL"].error_messages["required"] = u"file is required"
#         self.fields["fileURL"].error_messages["blank"] = u"file cannot be blank"
#         self.fields["title"].error_messages["required"] = u"title is required"
#         self.fields["title"].error_messages["blank"] = u"title cannot be blank"
#         self.fields["meme_type"].error_messages["required"] = u"meme type is required"
#         self.fields["meme_type"].error_messages["blank"] = u"meme type cannot be blank"


class MemeFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Meme
        fields = ['title']
