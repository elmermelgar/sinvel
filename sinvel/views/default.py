from pyramid.response import Response
from pyramid.renderers import render_to_response
from pyramid.view import view_config
from pyramid.security import NO_PERMISSION_REQUIRED,Authenticated
from ziggurat_foundations.ext.pyramid.sign_in import ZigguratSignInSuccess
from sqlalchemy.exc import DBAPIError
from ..models.models import Empleado
from ..models import Venta
from ..models import get_session_callable
from ..models import ResourceFactory


class Vista(object):


    def __init__(self, request):
        self.request = request
        #emp=Empleado()
        self.user=self.request.user.user_name
        #print(request.authenticated_userid)
        #request.session.expunge('empleado')
        self.emp=request.session['grupo']
        #empl=Empleado()
        #empl=emp


    @view_config(route_name='home', renderer='../templates/home.jinja2', permission=NO_PERMISSION_REQUIRED)
    def my_view(self):
        items_ventas = self.request.dbsession.query(Venta).all()
        #ResourceFactory(request)
        return {'one': 'one', 'ventas': items_ventas}


    @view_config(route_name='inicio', renderer='../templates/examples/inicio.jinja2',  permission='view')
    def inicio(self):
        return {'one': 'one', 'user': self.user }

    @view_config(route_name='forms', renderer='../templates/examples/forms.jinja2', permission='view')
    def forms(request):
        return {'one': 'one', 'user': 'sinvel'}

    @view_config(route_name='tables', renderer='../templates/examples/tables.jinja2', permission='view')
    def tables(request):
        return {'one': 'one', 'user': 'sinvel'}

    @view_config(route_name='panels', renderer='../templates/examples/panels.jinja2', permission='view')
    def tables(request):
        return {'one': 'one', 'user': 'sinvel'}

    @view_config(route_name='wizard', renderer='../templates/examples/wizard.jinja2', permission='view')
    def tables(request):
        return {'one': 'one', 'user': 'sinvel'}



db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_sinvel_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
