from datetime import date

from pyramid.view import view_config
from ..models import Importacion,ControlEmpresa,Reparacion,TipoReparacion,Taller,EstadoVeh,Bodega,Empleado,Vehiculo,DetalleImportacion,Remolque,TipoRemolque,DetalleControlEmpresa,UbicacionBodega,Nivel,Ubicacion
import jsonpickle
import json
from sqlalchemy.exc import DBAPIError
import transaction
from pyramid.httpexceptions import HTTPFound
from sqlalchemy.sql import func
from pyramid_mailer.message import Message
from sqlalchemy.sql.expression import literal
from sqlalchemy.orm import create_session

from sqlalchemy import *
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import create_session
from sqlalchemy import create_engine
from ..models import get_engine
import time


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

    @view_config(route_name='remolques', request_method='GET', renderer='json')
    def all_json_models(self):
        remolques = self.request.dbsession.query(Remolque).all()

        json_models = jsonpickle.encode(remolques,max_depth=4)
        print(json_models)
        return {'json_models': json_models}

    @view_config(route_name='registro_control', renderer='../templates/salida_reparacion/registro_control.jinja2',
                 request_method='GET')
    def registroControl(self):
        remolques = None
        salidas = None
        try:

            empleado = self.request.dbsession.query(Empleado).filter(Empleado.ID_EMPLEADO == self.user.id).one()
            remolques = self.request.dbsession.query(Remolque).filter(Remolque.ID_BODEGA == empleado.ID_BODEGA)\
                .filter(Remolque.DISPONIBLE == 1)
            salidas = self.request.dbsession.query(DetalleControlEmpresa,Vehiculo,Reparacion,UbicacionBodega,Ubicacion,Nivel).\
                 join(Reparacion).join(Vehiculo)\
                .filter(DetalleControlEmpresa.ID_VEHICULO==UbicacionBodega.ID_VEHICULO)\
                .filter(UbicacionBodega.ID_UBICACION==Ubicacion.ID_UBICACION)\
                .filter(Ubicacion.ID_NIVEL==Nivel.ID_NIVEL)\
                .filter(Nivel.ID_BODEGA==empleado.ID_BODEGA)\
                .filter(DetalleControlEmpresa.ID_CONTROL==None)\
                .filter(DetalleControlEmpresa.TIPO_CONTROL_DET=='SALREP').all()


        except DBAPIError:
            print('Error al recuperar los remolques')
        return {'salidas': salidas, 'remolques': remolques}

    @view_config(route_name='registro_control_guardar',request_method='POST')
    def registroControlSave(self):
        settings = {'sqlalchemy.url': 'mysql://root:admin@localhost:3306/sinvel_2'}
        engine = get_engine(settings)
        connection = engine.raw_connection()
        cursor = connection.cursor()

        control=ControlEmpresa()
        id_remolque=self.request.POST['ID_REMOLQUE']
        descripcion_control=self.request.POST['DESCRIPCION_CONTROL']
        control.DESCRIPCION_CONTROL=descripcion_control
        control.ID_REMOLQUE=id_remolque
        control.TIPO_CONTROL='SALREP'
        control.FECHA_CONTROL=time.strftime("%x")
        control.HORA_CONTROL=time.strftime("%H:%M:%S")
        self.request.dbsession.add(control)
        transaction.commit()
        query = self.request.dbsession.query(func.max(ControlEmpresa.ID_CONTROL).label('id_control_empresa')).one()
        id_ctrl_emp = query.id_control_empresa
        ids_det_control=self.request.params.getall("selected_vehiculos")
        try:
            for id_det_ctrl_emp in ids_det_control:
                args=[int(id_det_ctrl_emp),id_ctrl_emp,0]
                result_args =cursor.callproc('sp_update_sal_rep',args)
                print(result_args[0])
        except DBAPIError:
            print('Error al realizar la transaccion')
        finally:
            cursor.close()
            connection.commit()
        return HTTPFound(location='/salida_reparacion/registro_control')

    @view_config(route_name='aprobar_salidas', renderer='../templates/salida_reparacion/aprobar_salidas.jinja2',
                 request_method='GET')
    def aprobarSalidas(self):
        remolques = None
        salidas = None
        try:

            empleado = self.request.dbsession.query(Empleado).filter(Empleado.ID_EMPLEADO == self.user.id).one()

            salidas = self.request.dbsession.query(DetalleControlEmpresa, Vehiculo, ControlEmpresa, UbicacionBodega,
                                                   Ubicacion, Nivel). \
                join(ControlEmpresa).join(Vehiculo) \
                .filter(DetalleControlEmpresa.ID_VEHICULO == UbicacionBodega.ID_VEHICULO) \
                .filter(UbicacionBodega.ID_UBICACION == Ubicacion.ID_UBICACION) \
                .filter(Ubicacion.ID_NIVEL == Nivel.ID_NIVEL) \
                .filter(Nivel.ID_BODEGA == empleado.ID_BODEGA) \
                .filter(DetalleControlEmpresa.ID_EMPLEADO == None) \
                .all()


        except DBAPIError:
            print('Error al recuperar los remolques')
        return {'salidas': salidas}

    @view_config(route_name='aprobar_salidas_guardar', request_method='POST')
    def aprobarSalidasSave(self):
        settings = {'sqlalchemy.url': 'mysql://root:admin@localhost:3306/sinvel_2'}
        engine = get_engine(settings)
        connection = engine.raw_connection()
        cursor = connection.cursor()
        empleado = self.request.dbsession.query(Empleado).filter(Empleado.ID_EMPLEADO == self.user.id).one()

        ids_det_control = self.request.params.getall("selected_vehiculos")
        try:
            for id_det_ctrl_emp in ids_det_control:
                args = [int(id_det_ctrl_emp),empleado.ID_EMPLEADO, 0]
                result_args = cursor.callproc('sp_aprobar_salidas', args)
                print(result_args[0])
        except DBAPIError:
            print('Error al realizar la transaccion')
        finally:
            cursor.close()
            connection.commit()
        return HTTPFound(location='/salida_reparacion/aprobar_salidas')


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

