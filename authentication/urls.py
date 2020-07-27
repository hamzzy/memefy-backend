
from django.urls import path

from authentication.views import RegisterView, LoginView

urlpatterns = [
    path('sign_up/', RegisterView.as_view(), name='sign_up'),
    path('sign_in/',LoginView.as_view(), name='sign_in'),
    ]
