from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("rb/", views.rb, name="rb"),
    path("help/", views.help_for_people, name="help")
]
