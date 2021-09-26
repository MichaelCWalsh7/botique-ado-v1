from django.shortcuts import render  # noqa: F401
from .models import Product

# Create your views here.


def all_products(request):
    """A view to (a kill) show all products in cluding sorting and search queiries """

    products = Product.objects.all()

    context = {
        'products': products,
    }

    return render(request, 'products/products.html', context)
