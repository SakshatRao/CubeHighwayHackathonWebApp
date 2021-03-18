from django.contrib import admin
from django.conf.urls import include
from django.urls import re_path

from . import views

app_name = 'menu'

urlpatterns = [
    re_path(r'^$', views.menu_view, name = 'menu'),
    re_path(r'^item/$', views.item_view, name = 'item'),
    re_path(r'^order_item/$', views.order_item_view, name = 'order_item'),
    re_path(r'^checkout/$', views.checkout_view, name = 'checkout'),
    re_path(r'^payment/$', views.payment_view, name = 'payment'),
    re_path(r'^show_orders/$', views.show_orders_view, name = 'show_orders'),
]