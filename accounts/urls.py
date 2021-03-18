from django.urls import re_path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from . import views

app_name = 'accounts'

urlpatterns = [
    re_path(r'^signup/$', views.signup_view, name = 'signup'),
    re_path(r'^login/$', views.login_view, name = 'login'),
    re_path(r'^logout/$', views.logout_view, name = 'logout'),
    re_path(r'^edit/$', views.edit_view, name = 'edit'),
]