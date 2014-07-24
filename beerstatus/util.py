import json
from django.core.serializers.json import DjangoJSONEncoder
from tastypie.serializers import Serializer

class PrettyJSONSerializer(Serializer):
    """ pretty printed serializer as suggested in tastypie cookbook.

        Should be enabled if debug is true.
    """
    json_indent = 2

    def to_json(self, data, options=None):
        options = options or {}
        data = self.to_simple(data, options)
        return json.dumps(data, cls=DjangoJSONEncoder,
                sort_keys=True, ensure_ascii=False, indent=self.json_indent)


def validate_integer(value):
    """ Validates that the input is a valid integer.

    seems to be alko policy _for now_ to have their db keys as integers

    for our purposes it's always a string anyway so we store it as one
    """
    try:
        int(value)
    except ValueError:
        raise ValidationError("%s should be a valid number" % value)

def validate_takes_one_string(value):
    """ Validates that the argument contains %s at least once.
    """
    try:
        value % ""
    except TypeError:
        raise ValidationError("%s should cointain \%s once!" % value)

def jsonp_response_if_requested(function):
    """ decorator for simply serving jsonp to GET requests
    """
    def decorator(request, *args, **kwargs):
        response = func(request, *args, **kwargs)
        if 'callback' in request.REQUEST and request.method == "GET":
            data = '%s(%s);' % (request.REQUEST['callback'], response.content)
            return HttpResponse(data, "text/javascript")
        return resp
    return decorator

