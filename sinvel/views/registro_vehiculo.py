from pyramid.view import view_config
from ..models import Importacion


class RegistroVehiculo(object):
    def __init__(self,request):
        self.request=request
        self.user=request.user

    @view_config(route_name='registrar_vehiculo')
    def createRegistro(self):
        id_importacion=self.request.matchdict['id_importacion']
        importacion=self.request.dbsession.query(Importacion).filter(Importacion.ID_IMPORTACION==id_importacion).all()
        print(importacion)



