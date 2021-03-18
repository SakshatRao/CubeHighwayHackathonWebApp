from django.contrib import admin
from django.conf.urls import include
from django.urls import re_path
from . import views

app_name = 'customer'

urlpatterns = [
    re_path(r'^$', views.homepage_view, name = 'homepage'),
]