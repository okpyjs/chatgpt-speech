from customuser.views import UserRegistrationView
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import AudioView, ChatView, MailVerify, StripeInvoce, UserInfo

urlpatterns = [
    path("chat/", ChatView.as_view(), name="mydata-view"),
    path("audio/", AudioView.as_view(), name="audio-view"),
    path("mail-verify/", MailVerify.as_view(), name="mail-verify"),
    path("stripe-invoce/", StripeInvoce.as_view(), name="stripe-invoce"),
    path("userinfo/", UserInfo.as_view(), name="userinfo"),
    path("change-userinfo/", UserInfo.as_view(), name="change-userinfo")
    # path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    # path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
