from rest_framework import serializers
from .models import User


class Userserilizer(serializers.ModelSerializer):
    '''
    user serilizer
    '''

    class Meta:
        model = User
        field = ['email', 'name']
