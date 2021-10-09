from django.shortcuts import render, redirect, reverse, get_object_or_404  # noqa: E501
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category

# Create your views here.


def all_products(request):
    """A view to (a kill) show all products in cluding sorting and search queiries """    # noqa: E501

    products = Product.objects.all()  # pylint: disable=maybe-no-member
    query = None  # ensure no error occurs when loading products page without a search term.  # noqa: E501
    categories = None

    if request.GET:
        if 'category' in request.GET:
            # categories in html page are split by commas to facilitate this
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)  # pylint: disable=maybe-no-member  # noqa: E501

        # below is labelled 'q' as that is it's labelled in the search form on the base template  # noqa: E501
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")  # noqa: E501
                return redirect(reverse('products'))

            # the 'i' before queries makes make it case INSENSITIVE!!!
            queries = Q(name__icontains=query) | Q(description__icontains=query)  # noqa: E501
            products = products.filter(queries)

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
    }

    return render(request, 'products/products.html', context)


def product_details(request, product_id):
    """A view to (a kill) show individual product details """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)
