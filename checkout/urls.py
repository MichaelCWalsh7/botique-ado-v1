# pylint: disable=missing-module-docstring,unused-import
from django.contrib import admin  # noqa: F401
from django.urls import path
from . import views

urlpatterns = [
    path('', views.checkout, name='checkout')
]
