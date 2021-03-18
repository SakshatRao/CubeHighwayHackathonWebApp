from django.shortcuts import render
from utils.access import http_dict_func, customer_access

# Create your views here.

# Customer Homepage (Requires login)
@customer_access()
def homepage_view(request):
    http_dict = http_dict_func(request)
    return render(request, 'customer/homepage.html', http_dict)