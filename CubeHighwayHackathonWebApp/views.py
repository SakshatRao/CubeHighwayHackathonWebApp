from django.http import HttpResponse
from django.shortcuts import render
from utils.access import http_dict_func

def homepage_view(request):
    return render(request, "homepage.html", http_dict_func(request))

# If unauthorization is detected
def unauthorized_view(request):
    return render(request, 'unauthorized.html', http_dict_func(request))