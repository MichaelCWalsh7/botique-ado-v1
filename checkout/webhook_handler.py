# pylint: disable=missing-module-docstring,invalid-name,no-member,broad-except
import json
import time
from django.http import HttpResponse

from products.models import Product
from .models import Order, OrderLineItem


class StripeWH_Handler:
    """
    Handle Stripe webhooks
    """
    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200
        )

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook event
        """
        # pylint: disable=unused-variable
        # Initializes variables from payment intent object to create a order
        # in case the form wasn't submitted properly
        intent = event.data.object
        pid = intent.id
        bag = intent.metadata.bag
        save_info = intent.metadata.save_info  # noqa: F841

        billing_details = intent.charges.data[0].billing_details
        shipping_details = intent.shipping
        grand_total = round(intent.charges.data[0].amount / 100, 2)

        # Stripe will store blank fields as a blank string, but we want
        # these values to appear as 'None' in our database and thus run the
        # below code.
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        # First, we chekc to see if the form data is already in our database
        # In this case there's no extra action necessary and so we return a
        # and continue as normal. If it doens't exist we create it here in
        # the webhook.
        order_exists = False
        # the idea of the below while loop is that if the view is for some
        # reason slow to create the order than it could be duplicated, so
        # we try 5 times over 5 seconds to find the order.
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    # the iexact look up field checks for an exact, but case
                    # Insensitive match
                    full_name__iexact=shipping_details.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=shipping_details.phone,
                    country__iexact=shipping_details.address.country,
                    postcode__iexact=shipping_details.address.postal_code,
                    town_or_city__iexact=shipping_details.address.city,
                    street_address1__iexact=shipping_details.address.line1,
                    street_address2__iexact=shipping_details.address.line2,
                    county__iexact=shipping_details.address.state,
                    grand_total=grand_total,
                    original_bag=bag,
                    stripe_pid=pid,
                )
                order_exists = True
                break
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)
        if order_exists:
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: \
                Verified order already in database', status=200)
        else:
            order = None
            try:
                order = Order.objects.create(
                    full_name=shipping_details.name,
                    email=billing_details.email,
                    phone_number=shipping_details.phone,
                    country=shipping_details.address.country,
                    postcode=shipping_details.address.postal_code,
                    town_or_city=shipping_details.address.city,
                    street_address1=shipping_details.address.line1,
                    street_address2=shipping_details.address.line2,
                    county=shipping_details.address.state,
                    grand_total=grand_total,
                    original_bag=bag,
                    stripe_pid=pid,
                )
                for item_id, item_data in json.loads(bag).items():
                    product = Product.objects.get(id=item_id)
                    if isinstance(item_data, int):
                        order_line_item = OrderLineItem(
                            order=order,  # noqa: F821
                            product=product,
                            quantity=item_data,
                        )
                        order_line_item.save()
                    else:
                        for size, quantity in item_data['items_by_size'].items():  # noqa: E501
                            order_line_item = OrderLineItem(
                                order=order,  # noqa: F821
                                product=product,
                                quantity=quantity,
                                product_size=size,
                            )
                            order_line_item.save()
            except Exception as e:
                if order:
                    order.delete()
                return HttpResponse(content=f'Webhook received: \
                    {event["type"]} | ERROR: {e}', status=500)

        return HttpResponse(
            content=f'Webhook received: {event["type"]} | SUCCESS: Created \
            order in  webhook', status=200)

    def handle_payment_intent_failed(self, event):
        """
        Handle the payment_intent.failed webhook event
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200
        )
