import bcrypt
from pyramid.view import view_config
from sinvel.models import Importador,User,Empleado
import jsonpickle
from sqlalchemy.exc import DBAPIError
import transaction
from pyramid.httpexceptions import HTTPFound
from sqlalchemy.sql import func

class EmpleadoClase(object):
    def __init__(self,request):
        self.request = request
        self.user = User()

    @view_config(route_name='empleado_list', request_method='GET',renderer='../templates/crud/empleado.jinja2')
    def listEmpleado(self):
        empleados=None
        empleado = self.request.dbsession.query(Empleado).filter(Empleado.ID_USER == self.user.id).first()
        try:
            empleados=self.request.dbsession.query(Empleado).filter(Empleado.ID_BODEGA==empleado.ID_BODEGA).all()
        except:
            print('Error')
        return {'empleados': empleados}

    @view_config(route_name='empleado_create', request_method='GET', renderer='../templates/crud/empleado_create.jinja2')
    def createEmpleado(self):
        empleados = None

        empleado = self.request.dbsession.query(Empleado).filter(Empleado.ID_USER == self.user.id).first()
        try:
            empleados = self.request.dbsession.query(Empleado).filter(Empleado.ID_BODEGA == empleado.ID_BODEGA).all()
        except:
            print('Error')
        return {'value':''}


