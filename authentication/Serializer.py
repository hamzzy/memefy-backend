from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.http import request
from django.urls import reverse
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import serializers, validators
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.validators import UniqueValidator, ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView  # new

from .Utils import activation_email
from .models import CustomUser
from django.contrib.auth import authenticate

from rest_framework.exceptions import PermissionDenied
from rest_framework import status
from django.contrib.auth import password_validation
from rest_framework import exceptions
from django.utils.translation import gettext as _


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

        if user.is_verified == False:
            user = CustomUser.objects.get(email=email)
            token = RefreshToken.for_user(user).access_token
            # current_site = "memefy-back.herokuapp.com/"
            # relativeLink = reverse('email-verify')
            absurl = "http://localhost:3000/activate-email/"+str(token)

            context = {
                'url': absurl,
                'user': user,
            }

            activation_email(to=user, context=context)
            raise serializers.ValidationError(
                'User not verified another email sent for verification'
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

    def __init__(self, *args, **kwargs):
        super(ResetPasswordEmailRequestSerializer, self).__init__(*args, **kwargs)
        self.fields["email"].error_messages["required"] = u"email is required"
        self.fields["email"].error_messages["blank"] = u"email cannot be blank"

    class Meta:
        fields = ['email']


class UserAccountChangePasswordSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    old_password = serializers.CharField(write_only=True, help_text=_("Old password"))
    new_password = serializers.CharField(write_only=True, help_text=_("New password"))

    jwt_token = serializers.CharField(read_only=True)

    def __init__(self, *args, **kwargs):
        super(UserAccountChangePasswordSerializer, self).__init__(*args, **kwargs)
        self.fields["old_password"].error_messages["required"] = u"old password is required"
        self.fields["old_password"].error_messages["blank"] = u" old password  cannot be blank"
        self.fields["new_password"].error_messages["required"] = u"new password is required"
        self.fields["new_password"].error_messages["blank"] = u"new password  cannot be blank"

    def validate_new_password(self, new_password):
        password_validation.validate_password(new_password)
        return new_password

    def validate(self, attrs):
        old_password = attrs["old_password"]

        user = attrs["user"]
        if not user.check_password(old_password):
            raise exceptions.ValidationError({"old_password": _("Wrong old password")})

        return attrs

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        user = validated_data.pop("user")
        new_password = validated_data.pop("new_password")
        user.set_password(new_password)
        user.save()

        return user


class SetNewPasswordSerializer(serializers.Serializer):


    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(
        min_length=1, write_only=True)
    uidb64 = serializers.CharField(
        min_length=1, write_only=True)

    def __init__(self, *args, **kwargs):
        super(SetNewPasswordSerializer, self).__init__(*args, **kwargs)
        self.fields["password"].error_messages["required"] = u"password is required"
        self.fields["password"].error_messages["blank"] = u"password  cannot be blank"

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


class UserAccountUpdateSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    email = serializers.CharField(max_length=255,write_only=True)
    name = serializers.CharField(max_length=255,write_only=True)

    def __init__(self, *args, **kwargs):
        super(UserAccountUpdateSerializer, self).__init__(*args, **kwargs)
        self.fields["name"].error_messages["required"] = u"name is required"
        self.fields["name"].error_messages["blank"] = u"name cannot be blank"
        self.fields["email"].error_messages["required"] = u"email is required"
        self.fields["email"].error_messages["blank"] = u"email cannot be blank"

    def update(self, instance, validated_data):

        password = validated_data.pop('password', None)

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance







