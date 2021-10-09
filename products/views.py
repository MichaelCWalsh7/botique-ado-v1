from django.shortcuts import render, get_object_or_404  # noqa: F401
from .models import Product

# Create your views here.


def all_products(request):
    """A view to (a kill) show all products in cluding sorting and search queiries """    # noqa: E501

    products = Product.objects.all()  # pylint: disable=maybe-no-member

    context = {
        'products': products,
    }

    return render(request, 'products/products.html', context)


def product_details(request, product_id):
    """A view to (a kill) show individual product details """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)
