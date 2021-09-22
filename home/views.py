from django.shortcuts import render  # noqa: F401

# Create your views here.


def index(request):
    """A view to (a kill) return the index page"""

    return render(request, 'home/index.html')
