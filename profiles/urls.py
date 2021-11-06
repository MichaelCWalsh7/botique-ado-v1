# pylint: disable=missing-module-docstring,unused-import,no-member,line-too-long  # noqa: E501
from django.contrib import admin  # noqa: F401
from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('order_history/<order_number>', views.order_history, name='order_history')  # noqa: E501
]
