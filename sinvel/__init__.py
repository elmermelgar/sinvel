from pyramid.config import Configurator
from ziggurat_foundations.models import groupfinder
from pyramid.session import SignedCookieSessionFactory
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid_mailer import mailer_factory_from_settings
from pyramid_mailer.mailer import Mailer
from .models.root_factory import RootFactory
from .models.resource_factory import ResourceFactory
from pyramid.view import forbidden_view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import render_to_response
from pyramid.renderers import render
@forbidden_view_config()
def forbidden(request):
    if request.user is None:
        return HTTPFound(location='/login')
    else:
        #return Response('You are not allowed', status='403 Forbidden')
        result=render('/templates/errors/403.jinja2', {'foo':1},request=request)
        return Response(result, status='403 Forbidden')
def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    session_factory =  SignedCookieSessionFactory(
        settings['session.secret'],max_age=30000,
    )


    authn_policy = AuthTktAuthenticationPolicy(settings['session.secret'],
                                               callback=groupfinder)
    authz_policy = ACLAuthorizationPolicy()


    config = Configurator(settings=settings,root_factory='sinvel.models.RootFactory',
                          authentication_policy=authn_policy,
                          authorization_policy=authz_policy)
    # Set the session secret as per out ini file
    config.set_session_factory(session_factory)
    config.registry['mailer'] = Mailer.from_settings(settings)
    config.include('pyramid_jinja2')
    config.include('pyramid_mailer')
    config.include('pyramid_storage')
    config.include('pyramid_flash_message')

    config.include('.models')
    config.include('.routes')
    config.scan()
    return config.make_wsgi_app()
