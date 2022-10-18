from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta():
        model = User
        fields = ['email', 'username', 'password', 'mobile']

    def validate(self, attrs):
        email = User.objects.filter(email=attrs['email']).exists()
        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError(
                'user name must has alphanumaric characters')

        if email:
            raise serializers.ValidationError(
                'email already exists')

        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta():
        model = User
        fields = ['token']


class LoginSerializer(serializers.ModelSerializer):
    tokens = serializers.CharField(max_length=555, read_only=True)
    password = serializers.CharField(min_length=8, write_only=True)
    email = serializers.CharField(max_length=80)
    username = serializers.CharField(max_length=50, read_only=True)

    def validate(self, attrs):
        email = attrs['email']
        password = attrs.get('password', '')
        user = authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed(
                'bad credintials login failed')

        if not user.is_active:
            raise serializers.ValidationError(
                'Account not activated ,contact admin')

        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens()
        }

    class Meta():
        model = User
        fields = ['tokens', 'email', 'username', 'password']


class ResetPasswordRequestSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=80)

    class Meta:
        fields = ['email']
        model = User


class SetNewPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']
        model = User

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            uidb64 = attrs.get('uidb64')
            token = attrs.get('token')
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('reset link is invalid', 401)
            user.set_password(password)
            user.save()
            return (user)
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)
        return super().validate(attrs)
