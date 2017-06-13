from datetime import datetime
from datetime import date
from pyramid.view import view_config
from sqlalchemy import or_

from sinvel.models import Reparacion
from ..models import Importacion, EstadoVeh, Bodega, Empleado, Ubicacion, Importador, UbicacionBodega, Nivel, Vehiculo, \
    DetalleImportacion, Marca, Modelo, DetalleControlEmpresa, Remolque, TipoRemolque, ControlEmpresa
import jsonpickle
from sqlalchemy.exc import DBAPIError
import transaction
from pyramid.httpexceptions import HTTPFound
from ..models import get_engine
from sqlalchemy.sql import func
from pyramid_mailer.message import Message
import jsonpickle
import json
import time

import os
from pyramid.response import FileResponse


class RegistroVehiculo(object):
    def __init__(self, request):
        self.request = request
        self.emp = request.session['grupo']
        self.user = request.user
        self.importacion = Importacion()

    @view_config(route_name='registrar_vehiculo',request_method='GET', renderer='../templates/registrar_vehiculo.jinja2',permission='administrador,vendedor')
    def createRegistro(self):
        items_estado_vehiculo = self.request.dbsession.query(EstadoVeh).all()
        items_marcas = self.request.dbsession.query(Marca).all()
        return {'grupo': self.emp, 'items_estado_vehiculo': items_estado_vehiculo, 'importacion': self.importacion,
                'items_marcas': items_marcas}

    @view_config(route_name='buscar_importacion', renderer='json')
    def buscarImportacion(self):
        empleado = self.request.dbsession.query(Empleado).filter(Empleado.ID_USER == self.user.id).one()
        no_importacion = self.request.matchdict['id_importacion']
        try:
            self.importacion = self.request.dbsession.query(Importacion).filter(
                Importacion.NUM_REGISTRO == no_importacion).first()
        except DBAPIError:
            print('Error')
        if self.importacion is not None:
            importacion = {"ID_IMPORTACION": self.importacion.ID_IMPORTACION,
                           "IMPORTADOR": self.importacion.importador.NOMBRE,
                           "FECHA_IMPORTACION": str(self.importacion.FECHA_IMP)}
        else:
            importacion = {"ID_IMPORTACION": "",
                           "IMPORTADOR": "",
                           "FECHA_IMPORTACION": ""}
        # return {jsonpickle.encode(self.importacion,unpicklable=False)}
        return importacion

    @view_config(route_name='guardar_registro_vehiculo', request_method='POST',permission='administrador')
    def guardarRegistroVehiculo(self):
        try:
            empleado = self.request.dbsession.query(Empleado).filter(Empleado.ID_USER == self.user.id).one()
            data = self.request.POST
            vehiculo = Vehiculo()
            detalleImportacion = DetalleImportacion()
            detalleControlEmpresa = DetalleControlEmpresa()
            # Guardando el vehiculo
            for key, value in data.items():
                print(key, value)
                setattr(vehiculo, key, value)
            self.request.dbsession.add(vehiculo)
            # transaction.commit()
            query = self.request.dbsession.query(func.max(Vehiculo.ID_VEHICULO).label('id_vehiculo')).one()
            id_vehiculo = query.id_vehiculo
            # Guardando DetalleImportacion
            for key, value in data.items():
                print(key, value)
                setattr(detalleImportacion, key, value)
            detalleImportacion.ID_VEHICULO = id_vehiculo
            self.request.dbsession.add(detalleImportacion)
            # transaction.commit()
            # Guardando DetalleControlEmpresa
            detalleControlEmpresa.TIPO_CONTROL_DET = 'ENTRA'
            detalleControlEmpresa.ID_VEHICULO = id_vehiculo
            detalleControlEmpresa.ID_BODEGA = empleado.ID_BODEGA
            self.request.dbsession.add(detalleControlEmpresa)
            transaction.commit()
        except DBAPIError:
            return print('Ocurrio un error al insertar el registro')
        return HTTPFound(location='/RegistrarVehiculo')



    @view_config(route_name='models', request_method='GET', renderer='json')
    def all_json_models(self):
        current_brand = self.request.matchdict['id_marca']
        models = self.request.dbsession.query(Modelo).filter(Modelo.ID_MARCA == current_brand).all()
        json_models = jsonpickle.encode(models, max_depth=2)
        return {'grupo': self.emp, 'json_models': json_models}

    @view_config(route_name='registro_control_entrada', renderer='../templates/registrar_entrada.jinja2',
                 request_method='GET',permission='administrador')
    def registroControlEntradaPrimeraVez(self):
        remolques = None
        entradas = None
        try:

            empleado = self.request.dbsession.query(Empleado).filter(Empleado.ID_USER == self.user.id).one()
            remolques = self.request.dbsession.query(Remolque).filter(Remolque.ID_BODEGA == empleado.ID_BODEGA) \
                .filter(Remolque.DISPONIBLE == 0)
            entradas = self.request.dbsession.query(DetalleControlEmpresa, Vehiculo). \
                join(Vehiculo) \
                .filter(DetalleControlEmpresa.ID_CONTROL == None) \
                .filter(DetalleControlEmpresa.ID_EMPLEADO == None) \
                .filter(DetalleControlEmpresa.ID_BODEGA == empleado.ID_BODEGA) \
                .filter(DetalleControlEmpresa.TIPO_CONTROL_DET == 'ENTRA').all()

        except DBAPIError:
            print('Error al recuperar los remolques')
        return {'grupo': self.emp, 'entradas': entradas, 'remolques': remolques}

    @view_config(route_name='registro_entrada_control_guardar', request_method='POST',permission='administrador')
    def registroControlSave(self):

        id_user=self.user.id
        settings = {'sqlalchemy.url': 'mysql://root:admin@localhost:3306/sinvel_2'}
        engine = get_engine(settings)
        connection = engine.raw_connection()
        cursor = connection.cursor()

        control = ControlEmpresa()
        id_remolque = self.request.POST['ID_REMOLQUE']
        descripcion_control = self.request.POST['DESCRIPCION_CONTROL']
        control.DESCRIPCION_CONTROL = descripcion_control
        control.ID_REMOLQUE = id_remolque
        control.TIPO_CONTROL = 'ENTRAREP'
        control.FECHA_CONTROL = time.strftime("%Y-%m-%d")
        control.HORA_CONTROL = time.strftime("%H:%M:%S")
        self.request.dbsession.add(control)

        query = self.request.dbsession.query(func.max(ControlEmpresa.ID_CONTROL).label('id_control_empresa')).one()
        id_ctrl_emp = query.id_control_empresa
        ids_dce = self.request.params.getall("selected_vehiculos")
        try:
            empleado = self.request.dbsession.query(Empleado).filter(Empleado.ID_USER == id_user).one()
            for id_dce in ids_dce:
                dce = self.request.dbsession.query(DetalleControlEmpresa).filter(
                    DetalleControlEmpresa.ID_DET_CONTROL == id_dce).first()

                det_ctrl_emp = DetalleControlEmpresa()
                det_ctrl_emp.ID_VEHICULO = dce.vehiculo.ID_VEHICULO
                det_ctrl_emp.TIPO_CONTROL_DET = 'ENTRAREP'
                det_ctrl_emp.ID_CONTROL = id_ctrl_emp
                det_ctrl_emp.ID_EMPLEADO = empleado.ID_EMPLEADO
                det_ctrl_emp.ID_BODEGA = empleado.ID_BODEGA
                self.request.dbsession.add(det_ctrl_emp)

                # ACTUALIZAR EL ESTADO DE LA REPARACION DE LA SALIDA EN ESTADO SALEREP; ESTADO_REP_TALLER
                self.request.dbsession.query(Reparacion).filter(Reparacion.ID_DET_CONTROL == id_dce) \
                    .update({"ESTADO_REP_TALLER": 'Procesada'})

            transaction.commit()
        except DBAPIError:
            print('Error al realizar la transaccion')

        return HTTPFound(location='/entrada/registro_control_entrada_reparacion')



    @view_config(route_name='registro_control_entrada_reparacion', renderer='../templates/registrar_entrada_reparacion.jinja2',
                 request_method='GET')
    def registroControlEntradaReparacion(self):
        remolques = None
        entradas = None
        try:
            empleado = self.request.dbsession.query(Empleado).filter(Empleado.ID_USER == self.user.id).one()
            remolques = self.request.dbsession.query(Remolque).filter(Remolque.ID_BODEGA == empleado.ID_BODEGA) \
                .filter(Remolque.DISPONIBLE == 0)
            # SI ESTADO_REP_TALLER=NULL NO SE HA REGISTRADO LA ENTRADA A BODEGA NI CREADO EL COSTO DE LA REPARACION
            entradas = self.request.dbsession\
                .query(Vehiculo, DetalleControlEmpresa, Reparacion, UbicacionBodega,Ubicacion, Nivel, EstadoVeh) \
                .join(DetalleControlEmpresa).join(Reparacion).join(EstadoVeh).join(UbicacionBodega)\
                .join(Ubicacion).join(Nivel).filter(EstadoVeh.COD_ESTADO == '005')\
                .filter(or_(Reparacion.ESTADO_REP_TALLER==None, Reparacion.ESTADO_REP_TALLER == '')) \
                .filter(DetalleControlEmpresa.TIPO_CONTROL_DET == 'SALREP').all()

        except DBAPIError:
            print('Error al recuperar los remolques')
        return {'grupo': self.emp, 'entradas': entradas, 'remolques': remolques}

    @view_config(route_name='alerta_multa', renderer='../templates/alerta_multa.jinja2',
                 request_method='GET',permission='importador')
    def alertaMulta(self):

        vehiculos = None
        try:

            importador = self.request.dbsession.query(Importador).filter(Importador.ID_USER == self.user.id).one()

            vehiculos = self.request.dbsession.query(Vehiculo, EstadoVeh, Importacion, Importador, UbicacionBodega,
                                                     Ubicacion, Nivel) \
                .join(EstadoVeh).join(Importacion).join(Importador).join(UbicacionBodega).join(Ubicacion).join(Nivel) \
                .filter(Importador.ID_USER == self.user.id) \
                .filter(Ubicacion.DISPOONIBLE == 0) \
                .filter(
                (EstadoVeh.COD_ESTADO == '001') | (EstadoVeh.COD_ESTADO == '002') | (EstadoVeh.COD_ESTADO == '003') | (
                EstadoVeh.COD_ESTADO == '004') | (EstadoVeh.COD_ESTADO == '005')) \
                .all()
            now = datetime.now().date()

            for i in vehiculos:
                d1 = datetime.strptime(str(now), "%Y-%m-%d")
                d2 = datetime.strptime(str(i[4].FECHAINGRESO), "%Y-%m-%d")
                i[4].MULTA_EN = (15 - (d1 - d2).days)
                i[4].MULTA_EN_STR = str(15 - (d1 - d2).days) + ' días'
        except DBAPIError:
            print('Error al recuperar los remolques')
        return {'grupo': self.emp, 'vehiculos': vehiculos}



    @view_config(route_name='alerta_multa_cantidad_vehiculos', renderer='../templates/alerta_multa_cantidad_vehiculos.jinja2',
                     request_method='GET')
    def alertaMultaCantidadVehiculos(self):
        vehiculos = None
        try:
            importador = self.request.dbsession.query(Importador).filter(Importador.ID_USER == self.user.id).one()
            vehiculos = self.request.dbsession.query(UbicacionBodega, Bodega.NOMBRE_BODEGA,
                                                     func.count(UbicacionBodega.ID_VEHICULO)) \
                .join(Vehiculo).join(EstadoVeh).join(Importacion).join(Importador).join(Ubicacion).join(
                Nivel).join(Bodega) \
                .filter(Importador.ID_USER == self.user.id) \
                .filter(Ubicacion.DISPOONIBLE == 0) \
                .filter((EstadoVeh.COD_ESTADO == '001') | (EstadoVeh.COD_ESTADO == '002') | (
                EstadoVeh.COD_ESTADO == '003') | (EstadoVeh.COD_ESTADO == '004') | (EstadoVeh.COD_ESTADO == '005')) \
                .group_by(Bodega.ID_BODEGA).all()

        except DBAPIError:
            print('Error al recuperar los remolques')
        return {'grupo': self.emp, 'vehiculos': vehiculos}

    @view_config(route_name='generar_reporte', request_method='GET', renderer='../templates/registrar_vehiculo.jinja2')
    def generarReporte(self):
        mailer = self.request.registry['mailer']
        message = Message(subject="hello world",
                          sender="camaraipraspi3@gmail.com",
                          recipients=["polanco260593@gmail.com"],
                          body="hola Polanco desde pyramid")
        mailer.send_immediately(message, fail_silently=False)

        print('HOLA')
        print(os.path.dirname(os.path.abspath(__file__)))
        input_file = 'C:/Users/David/Documents/Pyramid/proyectos/sinvel/sinvel/reportes/registro_importacion.jrxml'
        output = 'C:/Users/David/Documents/Pyramid/proyectos/sinvel/sinvel/reportes/'

        con = {
            'driver': 'mysql',
            'username': 'root',
            'password': 'admin',
            'host': 'localhost',
            'database': 'sinvel',
            'port': '3306'
        }
        jasper = JasperPy()
        jasper.process(
            input_file,
            output,
            ["pdf"],
            {'ID_IMPORTACION': str(1), 'ID_USER': str(1)},
            con,
            'es_SV'
        ).execute()
        response = FileResponse(
            'C:/Users/David/Documents/Pyramid/proyectos/sinvel/sinvel/reportes/registro_importacion.pdf',
            request=self.request,
            content_type='application/pdf'
        )
        return response
