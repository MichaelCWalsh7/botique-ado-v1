# pylint: disable=missing-module-docstring,missing-function-docstring,line-too-long  # noqa: E501
from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment.")
        return redirect(reverse('products'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51Jo841KhzigfW6e3RYsQhgqugeGxqruSFcU4hxDCkMhpWM4F5tNNOu7P0EcNIQitRXp0jfqKe106LFMK6KI63IEL00tNyAzgK6',  # noqa: E501
        'client_secret': 'test client secret',
    }

    return render(request, template, context)
