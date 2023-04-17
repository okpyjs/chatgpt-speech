from django.urls import path

from .views import *

urlpatterns = [
    path("chat/", ChatView.as_view(), name="mydata-view"),
    path("audio/", AudioView.as_view(), name="audio-view"),
]
