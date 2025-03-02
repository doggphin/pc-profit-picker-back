from django.urls import path
from . import views

urlpatterns = [
    path("flips/", views.flips),
    path("test/", views.test)
]