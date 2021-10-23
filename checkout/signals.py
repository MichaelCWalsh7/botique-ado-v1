# pylint: disable=missing-module-docstring,unused-argument
# pylint: disable=pointless-string-statement
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import OrderLineItem


@receiver(post_save, sender=OrderLineItem)
def update_on_save(sender, instance, created, **kwargs):
    """
    Update order total on lineitem update/create
    sender = OrderLineItem, sender of signal
    instance = instance of the model that sent it
    created = boolean indicating if instance is new or being updated
    """
    instance.order.update_total()


@receiver(post_delete, sender=OrderLineItem)
def update_on_delete(sender, instance, **kwargs):
    """
    Update order total on lineitem delete
    sender = OrderLineItem, sender of signal
    instance = instance of the model that sent it
    created = boolean indicating if instance is new or being updated
    """
    instance.order.update_total()


"""
What's happening above? We're setting up code so that every time a line item
is added/removed, a signal is sent out, post_save or post_delete, which have
both been import above. The signal is then received by the receiver
(also imported above) which acts as a decorator that allows us to call the
update_total function from the Order model.
"""
