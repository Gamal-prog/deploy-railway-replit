from django.urls import path

from . import views


app_name = "main"

urlpatterns = [
    path("health/", views.health_check, name="health_check"),
    path("", views.course_list, name="course_list"),
    path("courses/<int:course_pk>/", views.course_detail, name="course_detail"),
    path(
        "courses/<int:course_pk>/videos/<int:video_pk>/",
        views.video_player,
        name="video_player",
    ),
]
