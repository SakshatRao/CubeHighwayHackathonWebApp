from django.contrib import admin
from django.conf.urls import include
from django.urls import re_path
from . import views

app_name = 'feedback'

urlpatterns = [
    re_path(r'^$', views.feedback_view, name = 'feedback'),
    re_path(r'^show_feedback/$', views.show_feedback_view, name = 'show_feedback'),
    re_path(r'^thankyou/$', views.thankyou_view, name = 'thankyou'),
]