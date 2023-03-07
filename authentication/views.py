from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.request import Request
from django.urls import reverse
import jwt
from django.conf import settings
import os
from .models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .utils import Util, CustomRedirect
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    LogoutSerializer,
    RequestVerifyEmailSerializer,
    EmailVerificationSerializer,
    SetNewPasswordSerializer,
    ResetPasswordEmailRequestSerializer
)


class RegisterAPIView(generics.GenericAPIView):
    """API View for registration"""
    serializer_class = RegisterSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(generics.GenericAPIView):
    """API View for login"""
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class LogoutAPIView(generics.GenericAPIView):
    """API View for logout"""
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated, ]

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EmailVerificationAPIView(views.APIView):
    serializer_class = EmailVerificationSerializer

    token_pram_conf = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_pram_conf])
    def get(self, request: Request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=['HS256'])
            User = get_user_model()
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
                return Response({'message': 'verified successfully'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': 'Account already verified'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Activation link expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return Response({'error': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)


class VerificationEmailRequestAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        user = request.user
        token = user.tokens()['access']
        relativeLink = reverse('emailverification')
        abs_url = f'http://{get_current_site(request).domain}{relativeLink}?token={str(token)}'
        email_body = f'Hi {user.username} use link below to verify \n{abs_url} \n\n\nNote: Your account will work 30 days without verification after that must be verified.'
        data = {
            'email_to': user.email,
            'email_body': email_body,
            'email_subject': 'Account Verification'
        }
        Util.send_email(data)
        return Response({'message': 'verification email sent successfully'}, status=status.HTTP_201_CREATED)


class ResetPasswordRequestEmailAPIView(generics.GenericAPIView):
    serializer_class = ResetPasswordRequestSerializer

    def post(self, request: Request):
        serializer = self.serializer_class(data=request.data)
        User = get_user_model()
        email = request.data['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            relativeLink = reverse(
                'pasword-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
            abs_url = f'http://{get_current_site(request).domain}{relativeLink}'
            email_body = f'Hi {user.username} use link below to reset your password \n{abs_url} '
            data = {
                'email_to': user.email,
                'email_body': email_body,
                'email_subject': 'Reset Password'
            }
            Util.send_email(data)
            return Response({'success': 'Reset password email sent successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'This email doesn\'t exist'}, status=status.HTTP_400_BAD_REQUEST)


class PasswordTokenCheckAPIView(generics.GenericAPIView):
    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            User = get_user_model()
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)
            return Response({'success': True, 'message': 'Credintials Valid', 'uidb64': uidb64, 'token': token})
        except DjangoUnicodeDecodeError:
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)


class SetNewpasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request: Request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)
