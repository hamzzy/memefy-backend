
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from authentication.views import RegisterView, LoginView, VerifyEmail, RequestPasswordResetEmail, PasswordTokenCheckAPI, \
    SetNewPasswordAPIView,UserAccountChangePasswordView,UserAccountUpdateView

urlpatterns = [
    path('sign_up', RegisterView.as_view(), name='sign_up'),
    path('sign_in',LoginView.as_view(), name='sign_in'),
    path('email-verify/', VerifyEmail.as_view(), name="email-verify"),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('request-reset-email/', RequestPasswordResetEmail.as_view(),name="request-reset-email"),
    path('password-reset/<uidb64>/<token>',PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete', SetNewPasswordAPIView.as_view(),name='password-reset-complete'),
    path("change-password/",UserAccountChangePasswordView.as_view(),name="change_password"),
    path("update-user", UserAccountUpdateView.as_view(), name="update-user")

]
