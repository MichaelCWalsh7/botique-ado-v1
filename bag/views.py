# pylint: disable=missing-module-docstring
from django.shortcuts import render, redirect, reverse, HttpResponse  # noqa: F401,E501

# Create your views here.


def view_bag(request):
    """A view to (a kill) render the bag contents page"""

    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """Add a quantity of the specified product to the shopping bag"""

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    # checks if the bag variable exists in the session or create it if not
    bag = request.session.get('bag', {})

    if size:
        if item_id in list(bag.keys()):
            # if the item is in the basket, we must check if it the same size,
            # so we can increment
            if size in bag[item_id]['items_by_size']:
                bag[item_id]['items_by_size'][size] += quantity
            else:
                # if not we can simply set the quantity as ordered.
                bag[item_id]['items_by_size'][size] = quantity
        else:
            # if the item isn't in the basket, this adds it as a dictionary
            # with the key of items by size. Allows us to have one item ID
            # per item, but still track different sizes. Clever.
            bag[item_id] = {'items_by_size': {size: quantity}}
    else:
        if item_id in bag in list(bag.keys()):
            # increments quantity if item is already in bag
            bag[item_id] += quantity
        else:
            # adds item to bag
            bag[item_id] = quantity

    # overwrites session variable with updated version
    request.session['bag'] = bag

    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """Adjust the qunatity of specified product by the specified amount"""

    quantity = int(request.POST.get('quantity'))
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    # checks if the bag variable exists in the session or create it if not
    bag = request.session.get('bag', {})

    if size:
        if quantity > 0:
            bag[item_id]['items_by_size'][size] = quantity
        else:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
    else:
        if quantity > 0:
            bag[item_id] = quantity
        else:
            bag.pop(item_id)

    # overwrites session variable with updated version
    request.session['bag'] = bag

    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """Remove the item from the shopping bag"""
    # pylint: disable=invalid-name,unused-variable,broad-except

    try:
        size = None
        if 'product_size' in request.POST:
            size = request.POST['product_size']
        # checks if the bag variable exists in the session or create it if not
        bag = request.session.get('bag', {})

        if size:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
        else:
            bag.pop(item_id)

        # overwrites session variable with updated version
        request.session['bag'] = bag

        return HttpResponse(status=200)

    except Exception as e:  # noqa: F841
        return HttpResponse(status=500)
