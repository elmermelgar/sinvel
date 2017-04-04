from pyramid.response import Response
from pyramid.view import view_config, view_defaults

from sinvel.models.models import Importador
from sinvel.views.user import db_err_msg
from ..models import Importacion
import transaction
from sqlalchemy.exc import DBAPIError
from pyramid.httpexceptions import HTTPFound

view_defaults(route_name='registroImportacion')

class RegistroImportacion(object):
    def __init__(self, request):
        self.request = request
        self.user = request.user

    @view_config(route_name='registroImportacion', renderer='../templates/importacion/registrar_importacion.jinja2', request_method='GET')
    def createRegistroImportacion(self):
        try:
            importadores = self.request.dbsession.query(Importador).all()
            #print('importadores', importadores)
            #importacion = Importacion()
            #importacion.importador=importadores
        except DBAPIError:
            return Response(db_err_msg, content_type='text/plain', status=500)
        return {'importadores':importadores}

    @view_config(route_name='registroImportacionGuardar', request_method='POST')
    def guardarRegistroImportacion(self):
        try:
            data = self.request.POST
            importacion = Importacion()
            for key, value in data.items():
                print(key, value)
                setattr(importacion, key, value)
            self.request.dbsession.add(importacion)
            transaction.commit()

        except DBAPIError:
            return print('Ocurrio un error al insertar el registro')
        return HTTPFound(location='/')
