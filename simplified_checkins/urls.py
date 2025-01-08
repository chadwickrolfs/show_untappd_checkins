from django.urls import path

from . import views


app_name = "sci"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("/checkin/", views.CheckinView.as_view, name="checkin"),
]
