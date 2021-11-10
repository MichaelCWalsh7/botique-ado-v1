# pylint: disable=missing-module-docstring,unused-import
from django.contrib import admin  # noqa: F401
from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name='products'),
    # the int in front of the product id variable ensures that the product
    # details view won't accept 'add/' as part of a product ID. This occurs
    # Django always uses the first url it finds a matching pattern for.
    path('<int:product_id>/', views.product_details, name='product_detail'),
    path('add/', views.add_product, name='add_product'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),  # noqa: E501
]
