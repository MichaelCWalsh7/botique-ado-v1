# pylint: disable=missing-module-docstring,unused-import,line-too-long
from django.contrib import admin  # noqa: F401
from django.urls import path
from .webhooks import webhook
from . import views

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('checkout_success/<order_number>', views.checkout_success, name='checkout_success'),  # noqa: E501
    path('cache_checkout_data/', views.cache_checkout_data, name='cache_checkout_data'),  # noqa: E501
    path('wh/', webhook, name='webhook'),
]
