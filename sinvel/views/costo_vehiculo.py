import bcrypt
from pyramid.view import view_config
from ..models import Costo,User,Vehiculo,Importacion,Importador,TipoCosto
import jsonpickle
from sqlalchemy.exc import DBAPIError
import transaction
from pyramid.httpexceptions import HTTPFound

from pyramid_mailer.message import Message

class costoVehiculo(object):
    def __init__(self,request):
        self.request = request
        self.user = User()
        self.item = Costo()
        self.query_costos = request.dbsession.query(Costo)
        self.query_tcostos = request.dbsession.query(TipoCosto)
        self.query_detalleCosto = request.dbsession.query(Vehiculo)


    @view_config(route_name='costo_veh', renderer='../templates/costos/costo_vehiculo.jinja2',request_method='GET')
    def costo_ve (self):
        id_vehiculo=self.request.matchdict['id_vehiculo']
        costos = self.query_costos.filter(Costo.ID_VEHICULO==id_vehiculo).all()



        return {'costos': costos}



    @view_config(route_name='detalle_costo', renderer='../templates/costos/detalle_costo.jinja2', request_method='GET')
    def detalle_costo(self):
        id_tipo_costo = self.request.matchdict['id_tipo_costo']
        det_cos = self.query_costos.filter(Costo.ID_TIPO_COSTO == id_tipo_costo).all()
        return {'det_cos': det_cos}


