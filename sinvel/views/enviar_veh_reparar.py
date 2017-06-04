import jsonpickle
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from sinvel.models import Taller, TipoReparacion


class RegistroVehiculo(object):
    def __init__(self,request):
        self.request=request
        self.user=request.user

    @view_config(route_name='enviarVehReparar', request_method='GET', renderer='../templates/importador/enviar_reparar.jinja2')
    def enviarVehReparacion(self):
        items_trep = self.request.dbsession.query(TipoReparacion).all()

        return {'items_trep':items_trep}

    @view_config(route_name='filterTalleres', request_method='GET', renderer='json')
    def tRepfilterTalleres(self):
        idtrep = self.request.matchdict['idtrep']

        talleres = self.request.dbsession.query(Taller).filter(Taller.ID_TIPO_REPARACION==idtrep).all()
        json_talleres = jsonpickle.encode(talleres,max_depth=2)
        return {'json_talleres': json_talleres}

    @view_config(route_name='enviarVehRepararGuardar', request_method='POST')
    def enviarVehRepSave(self):

        return HTTPFound(location='/inicio')