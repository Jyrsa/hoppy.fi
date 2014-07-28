from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^site.js$', views.site_js),
]
