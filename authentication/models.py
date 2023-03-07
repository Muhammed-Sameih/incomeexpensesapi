from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from rest_framework_simplejwt.tokens import RefreshToken


class UserManager(BaseUserManager):
    def create_user(self, username, email, mobile, password=None):
        """Method for create new user with based fields"""
        if username is None:
            raise TypeError('user name must exists!')
        if email is None:
            raise TypeError('Email address is required')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            mobile=mobile
        )
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, username, password=None):
        if password is None:
            raise TypeError('Password must not be None')

        user = self.create_user(
            username=username, mobile=None, email=email, password=password)
        user.is_superuser = True
        user.is_admin = True
        user.is_staff = True
        user.is_verified = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User class with email field used for login & custom fields like [username, mobile, password]"""
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    username = models.CharField(max_length=50, default="admin")
    mobile = models.CharField(max_length=11, null=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_tokens(self):
        "Method to get tokens for user"
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
