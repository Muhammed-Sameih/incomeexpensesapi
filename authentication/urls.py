from django.urls import path
from .views import (
    PasswordTokenCheckAPIView,
    RegisterAPIView,
    LoginAPIView,
    LogoutAPIView,
    RequestPasswordResetEmailAPIView,
    SetNewPasswordAPIView,
    VerifyEmailAPIView,
    RequestEmailVerificationAPIView
)

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('request-email-verification/', RequestEmailVerificationAPIView.as_view(),
         name='request-email-verification'),
    path('email-verify/', VerifyEmailAPIView.as_view(), name="email-verify"),
    path('request-reset-email/', RequestPasswordResetEmailAPIView.as_view(),
         name="request-reset-email"),
    path('password-reset/<uidb64>/<token>/',
         PasswordTokenCheckAPIView.as_view(), name='password-reset-confirm'),
    path('password-reset-complete', SetNewPasswordAPIView.as_view(),
         name='password-reset-complete'),
]
