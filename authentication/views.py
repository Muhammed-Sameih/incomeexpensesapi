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


class RequestEmailVerificationAPIView(generics.GenericAPIView):
    """API View for request verification email"""
    serializer_class = RequestVerifyEmailSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        serializer = self.serializer_class(data=request.data)
        user = request.user
        token = user.get_tokens()['access']
        relativeLink = reverse('email-verify')
        redirect_url = request.data.get('redirect_url', '')
        abs_url = f'http://{get_current_site(request).domain}{relativeLink}?token={str(token)}&redirect_url={str(redirect_url)}'
        email_body = f'Hi {user.username} use link below to verify \n{abs_url}\nNote: Your account will work 30 days without verification after that must be verified.'
        data = {
            'to_email': user.email,
            'email_body': email_body,
            'email_subject': 'Account Verification'
        }
        Util.send_email(data)
        return Response({'message': 'verification email sent successfully'}, status=status.HTTP_201_CREATED)


class VerifyEmailAPIView(views.APIView):
    """API View for verify account"""
    serializer_class = EmailVerificationSerializer

    def get(self, request: Request):

        token = str(request.GET.get('token'))
        redirect_url = request.GET.get('redirect_url', '')
        try:
            payload = jwt.decode(
                jwt=token, key=settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])

            if not user.is_verified:
                user.is_verified = True
                user.save()

            if redirect_url and len(redirect_url) > 3:
                return CustomRedirect(f'{redirect_url}?token_valid=True&message=Email verified&token={token}')
            else:
                return CustomRedirect(f"{os.environ.get('FRONTEND_URL', '')}?token_valid=True")

        except jwt.ExpiredSignatureError:
            if redirect_url and len(redirect_url) > 3:
                return CustomRedirect(f'{redirect_url}?token_valid=False&message=token expired')
            else:
                return CustomRedirect(f"{os.environ.get('FRONTEND_URL', '')}?token_valid=False&message=token expired")

        except jwt.exceptions.DecodeError:
            if redirect_url and len(redirect_url) > 3:
                return CustomRedirect(f'{redirect_url}?token_valid=False&message=token expired')
            else:
                return CustomRedirect(f"{os.environ.get('FRONTEND_URL', '')}?token_valid=False&message=invalid token")


class RequestPasswordResetEmailAPIView(generics.GenericAPIView):
    """API View for request password reset email"""
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data.get('email', '')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(
                request=request).domain
            relativeLink = reverse(
                'password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})

            redirect_url = request.data.get('redirect_url', '')
            absurl = 'http://'+current_site + relativeLink
            email_body = 'Hello, \n Use link below to reset your password  \n' + \
                absurl+"?redirect_url="+redirect_url
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Reset your passsword'}
            Util.send_email(data)
        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)


class PasswordTokenCheckAPIView(generics.GenericAPIView):
    """API View for check password token"""
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):

        redirect_url = request.GET.get('redirect_url')

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                if len(redirect_url) > 3:
                    return CustomRedirect(redirect_url+'?token_valid=False')
                else:
                    return CustomRedirect(os.environ.get('FRONTEND_URL', '')+'?token_valid=False')

            if redirect_url and len(redirect_url) > 3:
                return CustomRedirect(redirect_url+'?token_valid=True&message=Credentials Valid&uidb64='+uidb64+'&token='+token)
            else:
                return CustomRedirect(os.environ.get('FRONTEND_URL', '')+'?token_valid=False')

        except DjangoUnicodeDecodeError as identifier:
            try:
                if not PasswordResetTokenGenerator().check_token(user):
                    return CustomRedirect(redirect_url+'?token_valid=False')

            except UnboundLocalError as e:
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST)


class SetNewPasswordAPIView(generics.GenericAPIView):
    """API View for set new password"""
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)
