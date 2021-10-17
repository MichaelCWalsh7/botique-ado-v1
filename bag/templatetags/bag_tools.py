# pylint: disable=missing-module-docstring,missing-function-docstring
from django import template


register = template.Library()


@register.filter(name='calc_subtotal')
def calc_subtotal(price, quantity):
    return price * quantity
