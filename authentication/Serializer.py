from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers, validators
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.validators import UniqueValidator, ValidationError
from rest_framework_simplejwt.views import TokenObtainPairView  # new
from .models import CustomUser
from django.contrib.auth import authenticate

from rest_framework.exceptions import PermissionDenied
from rest_framework import status


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Registeration Serilizer
    Return:authentication Registered
    """

    email = serializers.CharField(max_length=255, validators=[
        UniqueValidator(
            queryset=CustomUser.objects.all(),
            message="user with this email already exist",
        )])
    name = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255, min_length=6, write_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'name', 'password')
        # read_only_fields = ('id',)

    def __init__(self, *args, **kwargs):
        super(CustomUserSerializer, self).__init__(*args, **kwargs)
        self.fields["name"].error_messages["required"] = u"name is required"
        self.fields["name"].error_messages["blank"] = u"name cannot be blank"
        self.fields["email"].error_messages["required"] = u"email is required"
        self.fields["email"].error_messages["blank"] = u"email cannot be blank"
        self.fields["password"].error_messages["blank"] = u"password cannot be blank"

        self.fields["password"].error_messages[
            "min_length"
        ] = u"password must be at least 8 chars"

    def create(self, validated_data):
        # Use the `create_user` method we wrote earlier to create a new user.
        # as long as the fields are the same, we can just use this

        return CustomUser.objects.create_user(**validated_data)

    # def update(self, instance, validated_data):
    #     instance.email = validated_data.get('email', instance.email)
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.save()
    #     return instance


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    name = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(write_only=True)
    tokens = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'password', 'tokens']

    def __init__(self, *args, **kwargs):
        super(LoginSerializer, self).__init__(*args, **kwargs)
        self.fields["name"].error_messages["required"] = u"name is required"
        self.fields["name"].error_messages["blank"] = u"name cannot be blank"
        self.fields["email"].error_messages["required"] = u"email is required"
        self.fields["email"].error_messages["blank"] = u"email cannot be blank"
        self.fields["password"].error_messages["blank"] = u"password cannot be blank"

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        user = authenticate(email=email, password=password)

        if not user:
            raise serializers.ValidationError(
                'email or password is incorrect'
            )

        if user.is_verified:
            raise serializers.ValidationError(
                'User not verified'
            )

        return {
            'email': user.email,
            'name': user.name,
            'tokens': user.tokens
        }


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = CustomUser
        fields = ['token']


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(
        min_length=1, write_only=True)
    uidb64 = serializers.CharField(
        min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)

            user.set_password(password)
            user.save()

            return (user)
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)
        return super().validate(attrs)
