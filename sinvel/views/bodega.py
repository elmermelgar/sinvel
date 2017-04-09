
from pyramid.view import view_config
from sqlalchemy.exc import DBAPIError
import transaction
import jsonpickle
from pyramid.httpexceptions import HTTPFound
from ..models import Bodega
from ..models import Nivel
from  ..models import Ubicacion
from sqlalchemy.sql import func


class Bodega_IU(object):
    def __init__(self,request):
        self.request=request
        self.user=request.user.user_name
        self.bodega = Bodega()
        self.nivel = Nivel()
        self.ubicacion = Ubicacion()

    @view_config(route_name='bodegas', renderer='../templates/bodega/bodegas.jinja2', request_method='GET')
    def bodegas(self):
        items_bodega = self.request.dbsession.query(Bodega).all()
        items_nivel = self.request.dbsession.query(Nivel).all()
        items_ubicacion = self.request.dbsession.query(Ubicacion).all()

        return {'bodegas': items_bodega, 'niveles': items_nivel, 'ubicaciones': items_ubicacion,'user':self.user}


