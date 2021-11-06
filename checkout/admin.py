# pylint: disable=missing-module-docstring,missing-class-docstring
# pylint: disable=unused-import
from django.contrib import admin  # noqa: F401
from .models import Order, OrderLineItem  # noqa: F401


class OrderLineItemAdminInline(admin.TabularInline):
    # Allows us to add/edit items in the admin from inside the Order model
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)


class OrderAdmin(admin.ModelAdmin):
    # Allows to access the above object in this admin model.
    inlines = (OrderLineItemAdminInline,)

    # Below we set certain fields to be readonly so that the integrity of an
    # order cannot be easliy compromised.
    readonly_fields = ('order_number', 'date', 'delivery_cost',
                       'order_total', 'grand_total', 'original_bag',
                       'stripe_pid',)

    # Allows to specify the order of the fields in admin which would otherwise
    # be adjusted by django due to the use of some readonly fields.
    fields = ('order_number', 'user_profile', 'date', 'full_name', 'email',
              'phone_number', 'country', 'postcode', 'town_or_city',
              'street_address1', 'street_address2', 'county', 'delivery_cost',
              'order_total', 'grand_total', 'original_bag', 'stripe_pid',)

    # restricts coumns that appear in the order list
    list_display = ('order_number', 'date', 'full_name', 'delivery_cost',
                    'order_total', 'grand_total', 'original_bag',
                    'stripe_pid',)

    # Reverse date ordering puts most recent orders at the top.
    ordering = ('-date',)


admin.site.register(Order, OrderAdmin)
