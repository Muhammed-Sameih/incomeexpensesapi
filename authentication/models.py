from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)
from rest_framework_simplejwt.tokens import RefreshToken
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, username, email, mobile=None, password=None):
        if username is None:
            raise TypeError('user name must exists!')
        if email is None:
            raise TypeError('email must exists!')
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            mobile=mobile
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password, mobile=None):
        if password is None:
            raise TypeError('password must exists!')
        user = self.create_user(
            username=username, email=email, mobile=mobile, password=password)
        user.is_staff = True
        user.superuser = True
        user.is_admin = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50)
    mobile = models.CharField(
        max_length=11, unique=True, null=True, blank=True, default=None)
    email = models.EmailField(max_length=80, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
