from tkinter import Image

from pyramid import request
from pyramid.view import view_config
import transaction
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound
from ..models import Bodega
from ..models import Nivel
from  ..models import Ubicacion
from ..models import Departamento
from ..models import  Vehiculo
from ..models import EstadoVeh
from sinvel.views.user import db_err_msg
from ..models import Municipio
from pyramid.httpexceptions import HTTPSeeOther
from sqlalchemy.exc import DBAPIError


class Bodega_IU(object):
    def __init__(self,request):
        self.request=request
        self.user=request.user.user_name
        self.bodega = Bodega()
        self.nivel = Nivel()
        self.ubicacion = Ubicacion()

    @view_config(route_name='registrarBodega', renderer='../templates/bodega/registrar_bodegas.jinja2',
                 request_method='GET')
    def createRegistroImportacion(self):
        try:
            departamentos = self.request.dbsession.query(Departamento).all()
            municipios = self.request.dbsession.query(Municipio).all()

        except DBAPIError:
            return Response(db_err_msg, content_type='text/plain', status=500)
        return {'departamentos': departamentos, 'municipios': municipios}

    @view_config(route_name='bodegas', renderer='../templates/bodega/bodegas.jinja2', request_method='GET')
    def bodegas(self):
        items_bodega = self.request.dbsession.query(Bodega).all()
        items_nivel = self.request.dbsession.query(Nivel).all()
        items_ubicacion = self.request.dbsession.query(Ubicacion).all()

        return {'bodegas': items_bodega, 'niveles': items_nivel, 'ubicaciones': items_ubicacion,'user':self.user}

    @view_config(route_name='detalle_bodega', renderer='../templates/bodega/detalle_bodega.jinja2', request_method='GET')
    def bodega_detalle(self):
        id = int(self.request.matchdict['id_bod'])
        items_bodega = self.request.dbsession.query(Bodega).get(id)
        items_nivel = self.request.dbsession.query(Nivel).filter_by(ID_BODEGA=items_bodega.ID_BODEGA)
        items_ubicacion = self.request.dbsession.query(Ubicacion).all()


        return {'bodega': items_bodega, 'user': self.user, 'niveles': items_nivel, 'ubicaciones': items_ubicacion}

    @view_config(route_name='registroBodegaGuardar', request_method='POST')
    def guardarRegistroBodega(self):
        try:
            data = self.request.POST
            bodega = Bodega()
            for key, value in data.items():
                setattr(bodega, key, value)
            self.request.dbsession.add(bodega)
            transaction.commit()

        except DBAPIError:
            print('Ocurrio un error al insertar el registro')
            print(db_err_msg)
            # return Response(db_err_msg, content_type='text/plain', status=500)
            return HTTPFound(location='/registro_bodega')
        return HTTPFound(location='/bodegas')

    @view_config(route_name='vehiculos', renderer='../templates/bodega/vehiculos.jinja2', request_method='GET')
    def vehiculos(self):
        items_vehiculos = self.request.dbsession.query(Vehiculo).all()

        return {'vehiculos': items_vehiculos, 'user': self.user}

    @view_config(route_name='ponerEnVenta', renderer='../templates/bodega/poner_en_venta.jinja2',
                 request_method='GET')
    def poner_en_venta(self):
        id = int(self.request.matchdict['id_veh'])
        items_vehiculo = self.request.dbsession.query(Vehiculo).get(id)
        items_estados = self.request.dbsession.query(EstadoVeh).all()


        return {'vehiculo': items_vehiculo, 'user': self.user, 'estados': items_estados}

    @view_config(route_name='ventaVehiculoActualizar', request_method='POST')
    def actualizarVehiculo(self):
        try:
            data = self.request.POST
            id = data.get('ID_VEHICULO')
            vehiculo = self.request.dbsession.query(Vehiculo).get(id)

            for key, value in data.items():
                if key == 'FOTO_VEH':
                    value = self.request.POST['FOTO_VEH'].file
                    value = value.read()
                setattr(vehiculo, key, value)
            transaction.commit()

        except DBAPIError:
            print('Ocurrio un error al actualizar el registro')
            print(db_err_msg)
            # return Response(db_err_msg, content_type='text/plain', status=500)
            return HTTPFound(location='/vehiculos')
        return HTTPFound(location='/vehiculos')