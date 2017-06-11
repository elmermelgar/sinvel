import bcrypt
from pyramid.view import view_config
from pyramid.renderers import render_to_response
from sinvel.models import TipoReparacion,User,Empleado,Group,UsersGroup,Bodega
from sqlalchemy.exc import DBAPIError
import transaction
from pyramid.httpexceptions import HTTPFound
from sqlalchemy.sql import func
from pyramid_mailer.message import Message

class TipoReparacionClase(object):
    def __init__(self,request):
        self.user = self.request.user.user_name
        self.emp = request.session['grupo']
        self.request = request

    @view_config(route_name='tipoReparacion_list', renderer='../templates/crud/tipoReparacion.jinja2',request_method='GET')
    def listtipoReparacion(self):

        tipoReparacion = self.request.dbsession.query(TipoReparacion).all()

        return {'grupo':self.emp, 'tipoRep': tipoReparacion}

    @view_config(route_name='tipoReparacion_create', request_method='GET', renderer='../templates/crud/tipoReparacion_create.jinja2')
    def createtipoReparacion(self):

        return {'grupo':self.emp, }

    @view_config(route_name='tipoReparacion_update', request_method='GET', renderer='../templates/crud/tipoReparacion_update.jinja2')
    def updatetipoReparacion(self):

        tipoReparacion=self.request.dbsession.query(TipoReparacion).get(self.request.matchdict['id_tipoRep'])

        return {'grupo':self.emp, 'tipoRep': tipoReparacion}


    @view_config(route_name='tipoReparacion_save', request_method='POST')
    def guardartipoReparacion(self):
        try:
            data = self.request.POST
            if self.request.POST.get('create')=='true':
                tipoRep=TipoReparacion()
                for key, value in data.items():
                    setattr(tipoRep, key, value)
                self.request.dbsession.add(tipoRep)

            else:
                data=self.request.POST
                id=data.get('ID_TIPO_REPARACION')
                tipoRep= self.request.dbsession.query(TipoReparacion).get(id)
                for key, value in data.items():
                    setattr(tipoRep, key, value)
            transaction.commit()

        except DBAPIError:
            return print('Ocurrio un error al insertar el registro')
        return HTTPFound(location='/tipoReparacion/list')

    @view_config(route_name='tipoReparacion_del', request_method='GET')
    def deletetipoReparacion(self):

        self.request.dbsession.query(TipoReparacion).filter(TipoReparacion.ID_TIPO_REPARACION == self.request.matchdict['id_tipoRep']).delete()
        transaction.commit()

        return HTTPFound(location='/tipoReparacion/list')
