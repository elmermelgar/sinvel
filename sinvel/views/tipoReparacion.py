import ctypes
import _mysql_exceptions
from pyramid.view import view_config
import transaction
from pyramid.response import Response
import sqlalchemy
from pyramid.view import view_config
from sinvel.models import TipoReparacion
from sqlalchemy.exc import DBAPIError
from pyramid.httpexceptions import HTTPFound

def Mbox(title, text, style):
    ctypes.windll.user32.MessageBoxW(0, text, title, style)

class TipoReparacionClase(object):
    def __init__(self,request):
        self.request=request
        self.user = self.request.user.user_name
        self.emp = request.session['grupo']

    @view_config(route_name='tipoReparacion_list', renderer='../templates/crud/tipoReparacion.jinja2',request_method='GET', permission='administrador')
    def listtipoReparacion(self):

        tipoReparacion = self.request.dbsession.query(TipoReparacion).all()

        return {'grupo':self.emp, 'tipoRep': tipoReparacion}

    @view_config(route_name='tipoReparacion_create', request_method='GET', renderer='../templates/crud/tipoReparacion_create.jinja2', permission='administrador')
    def createtipoReparacion(self):

        return {'grupo':self.emp, }

    @view_config(route_name='tipoReparacion_update', request_method='GET', renderer='../templates/crud/tipoReparacion_update.jinja2', permission='administrador')
    def updatetipoReparacion(self):

        tipoReparacion=self.request.dbsession.query(TipoReparacion).get(self.request.matchdict['id_tipoRep'])

        return {'grupo':self.emp, 'tipoRep': tipoReparacion}


    @view_config(route_name='tipoReparacion_save', request_method='POST', permission='administrador')
    def guardartipoReparacion(self):
        try:
            data = self.request.POST
            if self.request.POST.get('create')=='true':
                tipoRep=TipoReparacion()
                for key, value in data.items():
                    setattr(tipoRep, key, value)
                self.request.dbsession.add(tipoRep)

                self.request.flash_message.add('Se Creo el tipo de Reparación con exito!!', message_type='success')

            else:
                data=self.request.POST
                id=data.get('ID_TIPO_REPARACION')
                tipoRep= self.request.dbsession.query(TipoReparacion).get(id)
                for key, value in data.items():
                    setattr(tipoRep, key, value)

                self.request.flash_message.add('Se Actualizo el tipo de Reparación con exito!!', message_type='success')
            transaction.commit()

        except DBAPIError:
            self.request.flash_message.add('Ocurrio un error al insertar el registro!!', message_type='danger')
        return HTTPFound(location='/tipoReparacion/list')

    @view_config(route_name='tipoReparacion_del', request_method='GET', permission='administrador')
    def deletetipoReparacion(self):
        try:
            self.request.dbsession.query(TipoReparacion).filter(TipoReparacion.ID_TIPO_REPARACION == self.request.matchdict['id_tipoRep']).delete()
            transaction.commit()
        except sqlalchemy.exc.IntegrityError:
            self.request.flash_message.add('NO PUEDE ELIMINAR TIPO DE REPARACION!!', message_type='danger')

        return HTTPFound(location='/tipoReparacion/list')
