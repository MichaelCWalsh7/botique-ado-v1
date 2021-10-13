from django.contrib import admin  # noqa: F401
from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_bag, name='view_bag')
]
