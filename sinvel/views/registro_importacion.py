
from pyramid.response import Response
from pyramid.view import view_config, view_defaults

from sinvel.models.models import Importador
from sinvel.views.user import db_err_msg
from ..models import Importacion
from ..models import Bodega
import transaction
from sqlalchemy.exc import DBAPIError
from pyramid.httpexceptions import HTTPFound
from datetime import datetime
import sys

view_defaults(route_name='registroImportacion')

class RegistroImportacion(object):
    def __init__(self, request):
        self.request = request
        self.user = request.user
        self.emp = request.session['grupo']

    @view_config(route_name='registroImportacion', renderer='../templates/importacion/registrar_importacion.jinja2',
                 request_method='GET', permission='bodeguero')
    def createRegistroImportacion(self):
        try:
            importadores = self.request.dbsession.query(Importador).all()
            bodegas = self.request.dbsession.query(Bodega).all()

        except DBAPIError:
            self.request.flash_message.add('Ocurrio un error al guardar!!', message_type='danger')
            return HTTPFound(location=self.request.route_url('registroImportacion'))
        return {'grupo':self.emp, 'user':self.user.user_name, 'importadores':importadores, 'bodegas':bodegas}

    @view_config(route_name='registroImportacionGuardar', request_method='POST', permission='administrador')
    def guardarRegistroImportacion(self):
        try:
            data = self.request.POST
            importacion = Importacion()
            for key, value in data.items():
                #Convertir FECHA_IMP a fecha
                if key=='FECHA_IMP':
                    value = datetime.strptime(value, '%d-%m-%Y')
                #print(key, value)
                setattr(importacion, key, value)
            self.request.dbsession.add(importacion)
            transaction.commit()
            self.request.flash_message.add('Importación Guardada Correctamente!!', message_type='success')

        except DBAPIError:
            print('Ocurrio un error al insertar el registro')
            print(db_err_msg)
            self.request.flash_message.add('Ocurrió un error al guardar!!', message_type='danger')
            return HTTPFound(location=self.request.route_url('registroImportacion'))
        return HTTPFound(location='/RegistrarVehiculo')
