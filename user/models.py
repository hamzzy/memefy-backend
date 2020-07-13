from django.db import models
from django.contrib.auth.models import BaseUserManager


# Create your models here.

class Usermanager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('user must have an email')
        email = self.normalize_email(email)
        user = self.model(name=name, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def superuser(self, name, email, password):
        user = self.create_user(email, name, password)
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user


class User(models.Model):
    email = models.EmailField(max_length=225, unique=True)
    name = models.CharField(max_length=225)
    is_active = models.BooleanField(default=True)
    is_staf = models.BooleanField(default=False)
    objects = Usermanager()
    USERNAME_FIELD = ['email']
    REQUIRED_FIELD = ['name']

    def __str__(self):
        return self.name
