# pylint: disable=missing-module-docstring
from django.shortcuts import render  # noqa: F401

# Create your views here.


def view_bag(request):
    """A view to (a kill) render the bag contents page"""

    return render(request, 'bag/bag.html')
