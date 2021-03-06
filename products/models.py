# pylint: disable=missing-module-docstring,missing-class-docstring,line-too-long  # noqa: E501
# pylint: disable=missing-function-docstring,invalid-str-returned
from django.db import models


class Category(models.Model):

    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)
    # null=True & blank=True settings make it so the friendly name is optional  # noqa: E501
    friendly_name = models.CharField(max_length=254, null=True, blank=True)  # noqa: DJ01,E501

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):
    # connects the two class via foreign key and assures product doesn't
    # get deleted on category change/deletion
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)  # noqa: E501
    sku = models.CharField(max_length=254, null=True, blank=True)  # noqa: DJ01
    name = models.CharField(max_length=254)
    description = models.TextField()
    has_sizes = models.BooleanField(default=False, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)  # noqa: E501
    image_url = models.URLField(max_length=1024, null=True, blank=True)  # noqa: DJ01,E501
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name
