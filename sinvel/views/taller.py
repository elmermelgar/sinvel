import bcrypt
from pyramid.view import view_config
from sinvel.models import TipoReparacion,Taller
from sqlalchemy.exc import DBAPIError
import transaction
from pyramid.httpexceptions import HTTPFound

class TallerClase(object):
    def __init__(self,request):
        self.request = request

    @view_config(route_name='taller_list', renderer='../templates/crud/taller.jinja2',request_method='GET')
    def listtaller(self):

        taller = self.request.dbsession.query(Taller).all()

        return {'taller': taller}

    @view_config(route_name='taller_create', request_method='GET', renderer='../templates/crud/taller_create.jinja2')
    def createtaller(self):
        tipoRep=self.request.dbsession.query(TipoReparacion).all()

        return {'tipoRep':tipoRep}

    @view_config(route_name='taller_update', request_method='GET', renderer='../templates/crud/taller_update.jinja2')
    def updatetipoReparacion(self):
        tipoRep=self.request.dbsession.query(TipoReparacion).all()
        taller=self.request.dbsession.query(Taller).get(self.request.matchdict['id_taller'])

        return {'tipoRep':tipoRep, 'taller': taller}

    @view_config(route_name='taller_save', request_method='POST')
    def guardartipoReparacion(self):
        try:
            data = self.request.POST
            if self.request.POST.get('create')=='true':
                taller=Taller()
                for key, value in data.items():
                    setattr(taller, key, value)
                self.request.dbsession.add(taller)

            else:
                data=self.request.POST
                id=data.get('ID_TALLER')
                taller= self.request.dbsession.query(Taller).get(id)
                for key, value in data.items():
                    setattr(taller, key, value)
            transaction.commit()

        except DBAPIError:
            return print('Ocurrio un error al insertar el registro')
        return HTTPFound(location='/taller/list')

    @view_config(route_name='taller_del', request_method='GET')
    def deletetipoReparacion(self):
        self.request.dbsession.query(Taller).filter(Taller.ID_TALLER == self.request.matchdict['id_taller']).delete()
        transaction.commit()

        return HTTPFound(location='/taller/list')
