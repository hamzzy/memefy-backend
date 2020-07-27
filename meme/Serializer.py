from  rest_framework import serializers

from meme.models import MemeCategories


class MemeCategory(serializers.ModelSerializer):
    '''
    authentication serilizer
    '''
    class Meta:
        model = MemeCategories
        fields = ['id', 'name', 'slug']
        read_only_fields = ('id',)