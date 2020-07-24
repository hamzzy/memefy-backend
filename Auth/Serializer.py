from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    """
    Registeration Serilizer
    Return:Auth Registered
    """
    password = serializers.CharField(max_length=255, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'name', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        name = attrs.get('name', '')
        if not name.isalnum():
            raise serializers.ValidationError(
                'this  '
            )
        return attrs

    def save(self, validate_data):
        return User.objects.create_user(**validate_data)
