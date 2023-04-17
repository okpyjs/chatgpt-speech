from django.urls import path

from .views import MyDataView

urlpatterns = [
    path("mydata/", MyDataView.as_view(), name="mydata-view"),
]
