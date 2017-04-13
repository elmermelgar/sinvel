from pyramid.view import view_config
from ..models import Importacion,EstadoVeh,Empleado,Vehiculo,DetalleImportacion
import jsonpickle
from sqlalchemy.exc import DBAPIError
import transaction
from pyramid.httpexceptions import HTTPFound
from sqlalchemy.sql import func
from pyramid_mailer.message import Message


import os
from pyramid.response import FileResponse
from pyjasper.jasperpy import JasperPy

class RegistroVehiculo(object):
    def __init__(self,request):
        self.request=request
        self.user=request.user
        self.importacion=Importacion()

    @view_config(route_name='registrar_vehiculo',request_method='GET', renderer='../templates/registrar_vehiculo.jinja2')
    def createRegistro(self):
        items_estado_vehiculo=self.request.dbsession.query(EstadoVeh).all()
        return {'items_estado_vehiculo': items_estado_vehiculo,'importacion':self.importacion}


    @view_config(route_name='buscar_importacion', renderer='json')
    def buscarImportacion(self):
        empleado=self.request.dbsession.query(Empleado).filter(Empleado.ID_USER==self.user.id).one()
        id_importacion = self.request.matchdict['id_importacion']
        try:
            self.importacion=self.request.dbsession.query(Importacion).filter(Importacion.ID_IMPORTACION==id_importacion).filter(Importacion.ID_BODEGA==empleado.ID_BODEGA).first()
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
        #return {jsonpickle.encode(self.importacion,unpicklable=False)}
        return importacion

    @view_config(route_name='guardar_registro_vehiculo', request_method='POST')
    def guardarRegistroVehiculo(self):
        try:
                data = self.request.POST
                vehiculo = Vehiculo()
                detalleImportacion=DetalleImportacion()
                #Guardando el vehiculo
                for key, value in data.items():
                        print(key,value)
                        setattr(vehiculo, key, value)
                self.request.dbsession.add(vehiculo)
                transaction.commit()
                query=self.request.dbsession.query(func.max(Vehiculo.ID_VEHICULO).label('id_vehiculo')).one()
                id_vehiculo=query.id_vehiculo

                for key, value in data.items():

                        print(key,value)
                        setattr(detalleImportacion, key, value)
                detalleImportacion.ID_VEHICULO=id_vehiculo
                self.request.dbsession.add(detalleImportacion)
                transaction.commit()
        except DBAPIError:
            return print('Ocurrio un error al insertar el registro')
        return HTTPFound(location='/RegistrarVehiculo')

    @view_config(route_name='generar_reporte', request_method='GET',renderer='../templates/registrar_vehiculo.jinja2')
    def generarReporte(self):
        mailer = self.request.registry['mailer']
        message = Message(subject="hello world",
                          sender="camaraipraspi3@gmail.com",
                          recipients=["polanco260593@gmail.com"],
                          body="hola Polanco desde pyramid XD")
        mailer.send_immediately(message, fail_silently=False)

        print('HOLA')
        print(os.path.dirname(os.path.abspath(__file__)))
        input_file ='C:/Users/David/Documents/Pyramid/proyectos/sinvel/sinvel/reportes/registro_importacion.jrxml'
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
            {'ID_IMPORTACION':str(1),'ID_USER':str(1)},
            con,
            'es_SV'
        ).execute()
        response = FileResponse(
            'C:/Users/David/Documents/Pyramid/proyectos/sinvel/sinvel/reportes/registro_importacion.pdf',
            request=self.request,
            content_type='application/pdf'
        )
        return response

