from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import UserRegistrationView

# from .views import *

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
]
