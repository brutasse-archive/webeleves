from django.shortcuts import render_to_response
from django.template import RequestContext

def render(request, *args, **kwargs):
    """A shortcut over render to response:
    def my_view(request, *a, **kw):
        # Do some stuff
        # ...
        return render(request, 'template.html', locals()
    """
    kwargs['context_instance'] = RequestContext(request)
    return render_to_response(*args, **kwargs)
