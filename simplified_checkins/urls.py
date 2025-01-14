from django.urls import path

from . import views


app_name = "sci"
urlpatterns = [
    path("", views.IndexView.as_view(), name="sci-index"),
    path("checkins/", views.CheckinsView.as_view(), name="sci-checkins"),
    path(
        "check_checkins/",
        views.CheckinsView.as_view(),
        name="sci-check-checkins"
    ),
]
