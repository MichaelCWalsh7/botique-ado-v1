# pylint: disable=missing-module-docstring
from django.shortcuts import render, redirect, reverse, get_object_or_404  # noqa: E501
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from .models import Product, Category
from .forms import ProductForm

# Create your views here.


# pylint: disable=line-too-long
def all_products(request):
    """A view to (a kill) show all products in cluding sorting and search queiries """    # noqa: E501

    products = Product.objects.all()  # pylint: disable=maybe-no-member
    query = None  # ensure no error occurs when loading products page without a search term.  # noqa: E501
    categories = None
    sort = None  # pylint: disable=unused-variable
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey  # noqa: F841
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))

            if sortkey == 'category':
                sortkey = 'category__name'

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'

            products = products.order_by(sortkey)

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

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)


def product_details(request, product_id):
    """A view to (a kill) show individual product details """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)


def add_product(request):
    """
    Add a product to the store
    """
    form = ProductForm()
    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)
