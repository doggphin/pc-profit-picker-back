from django.urls import path
from . import views

urlpatterns = [
    path("flips/<int:budget>/", views.flips),
    path("test/", views.test)
]