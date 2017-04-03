from pyramid.view import view_config
from ..models import Importador
import jsonpickle
from sqlalchemy.exc import DBAPIError
import transaction
from pyramid.httpexceptions import HTTPFound
from sqlalchemy.sql import func

class AgregarImportador(object):
    def __init__(self,request):
        self.request=request


    @view_config(route_name='agregar_importador',request_method='GET',renderer='../templates/agregar_importador.jinja2')
    def createImportador(self):
         print('createImportador')
         return {'create':'create'}

    @view_config(route_name='guardar_importador', request_method='POST')
    def guardarImportador(self):
        try:

            data = self.request.POST
            vehiculo = Importador()

            for key, value in data.items():
                print(key, value)
                setattr(vehiculo, key, value)
            self.request.dbsession.add(vehiculo)
            transaction.commit()
            query = self.request.dbsession.query(func.max(Importador.ID_IMPORTADOR).label('id_IMPORTADOR')).one()
            id_vehiculo = query.id_vehiculo



        except DBAPIError:
            return print('Ocurrio un error al insertar el registro')
        return HTTPFound(location='/')





