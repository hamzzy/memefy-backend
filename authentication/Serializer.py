from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.views import TokenObtainPairView # new
from .models import CustomUser
from django.contrib.auth import authenticate


class RegisterSerializer(serializers.ModelSerializer):
    """
    Registeration Serilizer
    Return:authentication Registered
    """
    password = serializers.CharField(max_length=255, min_length=6, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'name', 'password']
        read_only_fields = ('id',)

    def validate(self, attrs):
        email = attrs.get('email', '')
        name = attrs.get('name', '')
        if name.isalnum():
            raise serializers.ValidationError(
                'this bjhbejhdb '
            )
        return attrs

    def save(self, validated_data):
        # Use the `create_user` method we wrote earlier to create a new user.
        return self.Meta.model.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=255)
    name = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128)
    tokens = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'name','password', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

            # Raise an exception if a
            # password is not provided.
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )
        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        return {
            'email': user.email,
            'name': user.name,
            'tokens': user.tokens
        }
