# pylint: disable=missing-module-docstring,missing-class-docstring,line-too-long,unused-import,no-member,unused-variable  # noqa: E501
import uuid  # noqa: F401

from django.db import models
from django.db.models import Sum  # noqa: F401
from django.conf import settings  # noqa: F401

from products.models import Product


class Order(models.Model):  # noqa: DJ08

    order_number = models.CharField(max_length=32, null=False, editable=False)
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = models.CharField(max_length=40, null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)  # noqa: DJ01,E501
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)  # noqa: DJ01,E501
    county = models.CharField(max_length=80, null=True, blank=True)  # noqa: DJ01,E501
    date = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)  # noqa: E501
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)  # noqa: E501
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)  # noqa: E501
    original_bag = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(max_length=254, null=False, blank=False, default='')  # noqa: E501

    def _generate_order_number(self):
        """
        Generate a random, unique number using UUID.
        """
        # function begins with an underscore to indicate that it is private
        # and only to be used by this class.
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        Update grand total each time a line item is added,
        accounting for delivery costs.
        """
        # Below we get the sum of a ll line item total fields for all
        # lineitem total fields for all lineitems on this order.
        self.order_total = self.lineitems.aggregate(Sum('lineitem_total'))['lineitem_total__sum'] or 0  # noqa: E501
        # Then, if the total is less than the delivery threshold, we multiply
        # it the percentage (in this case 10) to get the delivery charge.
        if self.order_total < settings.FREE_DELIVERY_THRESHOLD:
            self.delivery_cost = self.order_total * settings.STANDARD_DELIVERY_PERCENTAGE / 100  # noqa: E501
        else:
            # Otherwise it's 0
            self.delivery_cost = 0
        # Finally, we add this total to the delivery cost and we get the grand
        # total.
        self.grand_total = self.order_total + self.delivery_cost
        self.save()

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        # The below 'super' code executes the original django save method
        # after a unique order number has been generated.
        super().save(*args, **kwargs)

        def __str__(self):
            return self.order_number


class OrderLineItem(models.Model):  # noqa: DJ08
    order = models.ForeignKey(Order, null=False, blank=False, on_delete=models.CASCADE, related_name='lineitems')  # noqa: E501
    product = models.ForeignKey(Product, null=False, blank=False, on_delete=models.CASCADE)  # noqa: E501
    product_size = models.CharField(max_length=2, null=True, blank=True)  # XS, S, M, L, XL  # noqa: E501,DJ01
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False, editable=False)  # noqa: E501

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the lineitem total and update
        the order total.
        """
        self.lineitem_total = self.product.price * self.quantity
        # The below 'super' code executes the original django save method
        # after a unique order number has been generated.
        super().save(*args, **kwargs)

        def __str__(self):
            return f'SKU {self.product.sku} on order {self.order.order_number}'
