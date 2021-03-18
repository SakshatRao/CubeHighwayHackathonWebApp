from django.shortcuts import render
from utils.access import http_dict_func, admin_access

# Create your views here.

# Admin Homepage (Requires admin login)
@admin_access()
def homepage_view(request):
    http_dict = http_dict_func(request)
    return render(request, 'administration/homepage.html', http_dict)