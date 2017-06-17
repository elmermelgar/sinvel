import bcrypt
import sqlalchemy
from pyramid.view import view_config
from sinvel.models import TipoReparacion,Taller
from sqlalchemy.exc import DBAPIError
import transaction
from pyramid.httpexceptions import HTTPFound

class TallerClase(object):
    def __init__(self,request):
        self.request = request

    @view_config(route_name='taller_list', renderer='../templates/crud/taller.jinja2',request_method='GET', permission='administrador')
    def listtaller(self):

        taller = self.request.dbsession.query(Taller).all()

        return {'taller': taller}

    @view_config(route_name='taller_create', request_method='GET', renderer='../templates/crud/taller_create.jinja2', permission='administrador')
    def createtaller(self):
        tipoRep=self.request.dbsession.query(TipoReparacion).all()

        return {'tipoRep':tipoRep}

    @view_config(route_name='taller_update', request_method='GET', renderer='../templates/crud/taller_update.jinja2', permission='administrador')
    def updatetipoReparacion(self):
        tipoRep=self.request.dbsession.query(TipoReparacion).all()
        taller=self.request.dbsession.query(Taller).get(self.request.matchdict['id_taller'])

        return {'tipoRep':tipoRep, 'taller': taller}

    @view_config(route_name='taller_save', request_method='POST', permission='administrador')
    def guardartipoReparacion(self):
        try:
            data = self.request.POST
            if self.request.POST.get('create')=='true':
                taller=Taller()
                for key, value in data.items():
                    setattr(taller, key, value)
                self.request.dbsession.add(taller)

                self.request.flash_message.add('Se Creo el Taller con exito!!', message_type='success')

            else:
                data=self.request.POST
                id=data.get('ID_TALLER')
                taller= self.request.dbsession.query(Taller).get(id)
                for key, value in data.items():
                    setattr(taller, key, value)

                self.request.flash_message.add('Se Actualizo el Taller con exito!!', message_type='success')
            transaction.commit()

        except DBAPIError:
            return print('Ocurrio un error al insertar el registro')
        return HTTPFound(location='/taller/list')

    @view_config(route_name='taller_del', request_method='GET', permission='administrador')
    def deletetipoReparacion(self):
        try:
            self.request.dbsession.query(Taller).filter(Taller.ID_TALLER == self.request.matchdict['id_taller']).delete()
            transaction.commit()

        except sqlalchemy.exc.IntegrityError:
            self.request.flash_message.add('NO PUEDE ELIMINAR TALLER!!', message_type='danger')

        return HTTPFound(location='/taller/list')
