from .views import RegisterAPIView, EmailVerificationAPIView, VerificationEmailRequestAPIView, LoginAPIView, PasswordTokenCheckAPIView, ResetPasswordRequestEmailAPIView, SetNewpasswordAPIView
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('emailverification/', EmailVerificationAPIView.as_view(),
         name='emailverification'),
    path('request-verification-email/',
         VerificationEmailRequestAPIView.as_view(), name='request-verification-email'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('password-reset/<uidb64>/<token>/',
         PasswordTokenCheckAPIView.as_view(), name='pasword-reset-confirm'),
    path('request-password-reset-email/', ResetPasswordRequestEmailAPIView.as_view(),
         name='request-password-reset-email'),
    path('set-new-password/', SetNewpasswordAPIView.as_view(),
         name='set-new-password'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
