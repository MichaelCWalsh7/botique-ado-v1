# pylint: disable=missing-module-docstring
# pylint: disable=unused-import
from django.contrib import admin  # noqa: F401
from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_bag, name='view_bag'),
    path('add/<item_id>', views.add_to_bag, name='add_to_bag'),
]
