from customuser.views import UserRegistrationView
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import AudioView, ChatView, MailVerify

urlpatterns = [
    path("chat/", ChatView.as_view(), name="mydata-view"),
    path("audio/", AudioView.as_view(), name="audio-view"),
    path("mail-verify/", MailVerify.as_view(), name="mail-verify")
    # path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    # path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
