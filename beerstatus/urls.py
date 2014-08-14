from django.conf.urls import url
from . import views
from beerstatus.views import TemplateTrackingView

from django.conf import settings
GA_TRACKING_CODE = getattr(settings, "GA_TRACKING_CODE", "")

urlpatterns = [
    url(r'^$', TemplateTrackingView.as_view(
                                            template_name="beerstatus/index.html",
                                            tracking_code=GA_TRACKING_CODE)),
    url(r'^about/$', TemplateTrackingView.as_view(
                                            template_name="beerstatus/about.html",
                                            tracking_code=GA_TRACKING_CODE)),
    url(r'^site.js$', views.site_js),
]
