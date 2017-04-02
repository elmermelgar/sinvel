from pyramid.view import forbidden_view_config
from pyramid.view import notfound_view_config

@forbidden_view_config(renderer='../templates/errors/403.jinja2')
def notfound_view(request):
    request.response.status = 403
    return {}

@notfound_view_config(renderer='../templates/errors/404.jinja2')
def notfound_view(request):
    request.response.status = 404
    return {}
