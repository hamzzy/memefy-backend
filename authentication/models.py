import datetime

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
import uuid
# Create your models here.
from rest_framework_simplejwt.tokens import RefreshToken


class MyUserManager(BaseUserManager):
    def create_user(self, name, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            name=name,
            email=self.normalize_email(email)

        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, name, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            name,
            email,
            password
        )
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, null=False)
    name = models.CharField(max_length=225)
    email = models.EmailField(max_length=225, unique=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = MyUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def get_full_name(self):
        """
        This method is required by Django for things like handling emails.
        Typically this would be the user's first and last name. Since we do
        not store the user's real name, we return their username instead.
        """
        return self.name

    def get_short_name(self):
        """
        This method is required by Django for things like handling emails.
        Typically, this would be the user's first name. Since we do not store
        the user's real name, we return their username instead.
        """
        return self.name

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

