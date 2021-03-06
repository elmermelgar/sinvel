from pyramid.response import Response
from pyramid.renderers import render_to_response
from pyramid.view import view_config
from pyramid.security import NO_PERMISSION_REQUIRED,Authenticated, ALL_PERMISSIONS
from ziggurat_foundations.ext.pyramid.sign_in import ZigguratSignInSuccess
from sqlalchemy.exc import DBAPIError
from ..models.models import Empleado, Vehiculo
from ..models import Venta
from ..models import get_session_callable
from ..models import ResourceFactory
import _mysql_exceptions
from pyramid.view import view_config
import transaction
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound
from ..models import Bodega
from ..models import Nivel
from  ..models import Ubicacion
from ..models import Departamento
from ..models import  Vehiculo
from ..models import EstadoVeh
from ..models import DetalleControlEmpresa
from ..models import Venta
from ..models import Cliente
from ..models import Empleado
from ..models import User
from sinvel.views.user import db_err_msg
from ..models import Municipio
from pyramid.httpexceptions import HTTPSeeOther
from sqlalchemy.exc import DBAPIError
from datetime import datetime
import ctypes
from ..models import get_engine

class Vista(object):


    def __init__(self, request):
        self.request = request
        #emp=Empleado()

        #print(request.authenticated_userid)
        #request.session.expunge('empleado')
        if(self.request.user is not None):
            self.user = self.request.user.user_name
            self.emp = request.session['grupo']

        #empl=Empleado()
        #empl=emp


    @view_config(route_name='home', renderer='../templates/home.jinja2')
    def my_view(self):
        items_ventas = self.request.dbsession.query(Venta).all()
        #ResourceFactory(request)
        return {'one': 'one', 'ventas': items_ventas}


    @view_config(route_name='inicio', renderer='../templates/examples/inicio.jinja2',  permission=NO_PERMISSION_REQUIRED )
    def inicio(self):
        # self.request.flash_message.add('Registro Guardado Correctamente!!', message_type='success')
        # self.request.flash_message.add('Registro Guardado Parcialmente!!', message_type='warning')
        # self.request.flash_message.add('Error no se pudo guardar el registro!!', message_type='danger')
        # self.request.flash_message.add('Notificacion normal!!', message_type='inverse')

        return {'one': 'one', 'user': self.user, 'grupo':self.emp}

    @view_config(route_name='forms', renderer='../templates/examples/forms.jinja2', permission='view')
    def forms(request):
        return {'one': 'one', 'user': 'sinvel'}

    @view_config(route_name='tables', renderer='../templates/examples/tables.jinja2')
    def tables(request):
        return {'one': 'one', 'user': 'sinvel'}

    @view_config(route_name='vehiculos_buscar', renderer='../templates/examples/inicio_prueba.jinja2')
    def tables(self):
        vehiculos = self.request.dbsession.query(Vehiculo).all()
        print('**********************************************************')
        print(vehiculos)
        return {'vehiculos': vehiculos, 'user': self.user}

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
