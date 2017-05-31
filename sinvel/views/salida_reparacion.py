from pyramid.view import view_config
from ..models import Importacion,EstadoVeh,Empleado,Vehiculo,DetalleImportacion,Remolque,TipoRemolque
import jsonpickle
import json
from sqlalchemy.exc import DBAPIError
import transaction
from pyramid.httpexceptions import HTTPFound
from sqlalchemy.sql import func
from pyramid_mailer.message import Message


import os
from pyramid.response import FileResponse

class SalidaReparacion(object):
    def __init__(self,request):
        self.request=request
        self.user=request.user





    @view_config(route_name='verificar_remolque', renderer='../templates/salida_reparacion/verificar_remolque.jinja2', request_method='GET')
    def verificarRemolque(self):
        items_tipo_remolque=None
        remolques=None
        try:
            items_tipo_remolque=self.request.dbsession.query(TipoRemolque).all()
            empleado = self.request.dbsession.query(Empleado).filter(Empleado.ID_EMPLEADO == self.user.id).one()
            remolques = self.request.dbsession.query(Remolque).filter(Remolque.ID_BODEGA == empleado.ID_BODEGA).filter(Remolque.DISPONIBLE==1).all()
        except DBAPIError:
            print('Error al recuperar los remolques')

        return {'remolques': remolques, 'items_tipo_remolque': items_tipo_remolque}

    @view_config(route_name='buscar_tipo_remolque', renderer='../templates/salida_reparacion/verificar_remolque.jinja2',request_method='GET')
    def buscarRemolque(self):
        id_tipo_remolque = self.request.matchdict['id_tipo_remolque']
        print('test'+id_tipo_remolque)
        items_tipo_remolque = None
        remolques = None
        try:
            items_tipo_remolque = self.request.dbsession.query(TipoRemolque).all()
            empleado = self.request.dbsession.query(Empleado).filter(Empleado.ID_EMPLEADO == self.user.id).one()
            remolques = self.request.dbsession.query(Remolque).filter(Remolque.ID_BODEGA == empleado.ID_BODEGA).filter(
                Remolque.DISPONIBLE == 1).filter(Remolque.ID_TIPO_REMOLQUE==id_tipo_remolque).all()
        except DBAPIError:
            print('Error al recuperar los remolques')

        return {'remolques': remolques, 'items_tipo_remolque': items_tipo_remolque}


