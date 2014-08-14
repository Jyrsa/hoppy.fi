#write possible views here

from django.shortcuts import render_to_response
from beerstatus.api import AlkoLocationResource
from django.utils.safestring import mark_safe

from django.views.generic.base import TemplateView


class TemplateTrackingView(TemplateView):
    tracking_code = None

    def __init__(self, *args, **kwargs):
        self.tracking_code = kwargs.get("tracking_code")
        self.template_name = kwargs.get("template_name")

    def get_context_data(self, **kwargs):
        context = super(TemplateTrackingView, self).get_context_data(**kwargs)
        context['tracking_code'] = mark_safe(self.tracking_code)
        return context


def site_js(request):
    """ returns the JS file with the initial data
    """
    res = AlkoLocationResource()
    request_bundle = res.build_bundle(request=request)
    queryset = res.obj_get_list(request_bundle)

    bundles = []
    for obj in queryset:
        bundle = res.build_bundle(obj=obj, request=request)
        bundles.append(res.full_dehydrate(bundle, for_list=True))

    list_json = res.serialize(None, bundles, "application/json")

    return render_to_response('beerstatus/js/site.js', {
        # Other things here.
        "alko_list": mark_safe(list_json),
        },
        mimetype="text/javascript")
