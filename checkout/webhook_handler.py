# pylint: disable=missing-module-docstring,invalid-name,no-member,broad-except
import json
import time
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from products.models import Product
from profiles.models import UserProfile
from .models import Order, OrderLineItem


class StripeWH_Handler:
    """
    Handle Stripe webhooks
    """
    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, order):
        """
        Send the user a confirmation email
        """
        cust_email = order.email
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            # Below we initialize 'order' so we can use it's variables in the
            # email template
            {'order': order})
        body = render_to_string(
            'checkout/confirmation_emails/confirmation_email_body.txt',
            {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL})

        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [cust_email]
        )

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

        # Update profile information if save_info was checked
        profile = None
        # Grab username from metadata we added to stripe pid in checkouts view
        # cache_checkout_data function
        username = intent.metadata.username
        # If user is autheneticated, and save_info was checked, we retrieve
        # their profile and update the defaults
        if username != 'AnonymousUser':
            profile = UserProfile.objects.get(user__username=username)
            if save_info:
                profile.default_phone_number = shipping_details.phone
                profile.default_country = shipping_details.address.country
                profile.default_postcode = shipping_details.address.postal_code  # noqa: E501
                profile.default_town_or_city = shipping_details.address.city
                profile.default_street_address1 = shipping_details.address.line1  # noqa: E501
                profile.default_street_address2 = shipping_details.address.line2  # noqa: E501
                profile.default_county = shipping_details.address.state
                profile.save()

        # First, we check to see if the form data is already in our database
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
            # send confirmation before returning response to Stripe
            self._send_confirmation_email(order)
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: \
                Verified order already in database', status=200)
        else:
            order = None
            try:
                order = Order.objects.create(
                    full_name=shipping_details.name,
                    user_profile=profile,
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
        # send confirmation before returning response to Stripe
        self._send_confirmation_email(order)
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
