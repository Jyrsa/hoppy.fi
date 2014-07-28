from django.conf.urls import url
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="beerstatus/index.html")),
    url(r'^about/$', TemplateView.as_view(template_name="beerstatus/about.html")),
    url(r'^site.js$', views.site_js),
]
