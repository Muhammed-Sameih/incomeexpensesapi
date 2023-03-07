from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str, DjangoUnicodeDecodeError
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.utils.http import urlsafe_base64_decode


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer class for registeration by email, username, mobile & password"""
    email = serializers.EmailField(min_length=10, max_length=255)
    password = serializers.CharField(
        min_length=8, max_length=80, write_only=True)
    username = serializers.CharField(max_length=50, min_length=3)
    mobile = serializers.CharField(max_length=11, min_length=11)

    class Meta:
        model = User
        fields = ['username', 'mobile', 'email', 'password']

    def validate(self, attrs):
        "Validation method check if email used before & is mobile consist of nums only"
        email = attrs.get('email', '')
        mobile = attrs.get('mobile', '')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {'email': 'Email is already exist'})
        if not (mobile.isnumeric()):
            raise serializers.ValidationError(
                {'mobile': 'Mobile must consist of only numbers'})

        return super().validate(attrs)

    def create(self, validate_data):
        return User.objects.create_user(**validate_data)


class LoginSerializer(serializers.ModelSerializer):
    """Serializer class for login by email & password"""
    tokens = serializers.CharField(max_length=555, read_only=True)
    tokens = serializers.SerializerMethodField()
    password = serializers.CharField(min_length=8, write_only=True)
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=50, read_only=True)

    def get_tokens(self, obj):
        """Method to get tokens for user by using get_tokens method in User class by get user obj by email from data base."""
        user = User.objects.get(email=obj['email'])
        return {
            'access': user.get_tokens()['access'], 'refresh': user.get_tokens()['refresh']
        }

    def validate(self, attrs):
        "Validation method check if user exist by authenticate function & check if user account is active by user is_active attribute then return user email, username & tokens"
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
            'tokens': user.get_tokens()
        }

    class Meta():
        model = User
        fields = ['email', 'username', 'password', 'tokens']


class LogoutSerializer(serializers.Serializer):
    """Logout serializer class with refresh token, log out by blacklisting this token"""
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail('bad_token')


class RequestVerifyEmailSerializer(serializers.Serializer):

    redirect_url = serializers.CharField(max_length=500, required=False)

    class Meta:
        fields = ['redirect_url']


class EmailVerificationSerializer(serializers.ModelSerializer):
    """Verification email serializer class"""
    token = serializers.CharField(max_length=555)
    redirect_url = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    """Request email for reset password serializer class"""
    email = serializers.EmailField(min_length=2)

    redirect_url = serializers.CharField(max_length=500, required=False)

    class Meta:
        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    """Set new password serializer class"""
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(
        min_length=1, write_only=True)
    uidb64 = serializers.CharField(
        min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        """Validation method for check reset password token for user & add the new password if reset link is valid"""
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)

            user.set_password(password)
            user.save()

            return (user)
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)
        return super().validate(attrs)
