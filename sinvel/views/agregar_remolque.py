import bcrypt
from pyramid.view import view_config
from ..models import Remolque,User
from sinvel.views.user import db_err_msg
from sqlalchemy.exc import DBAPIError
import transaction
from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response

class AgregarRemolque(object):
    def __init__(self,request):
        self.request = request
        self.user = User()

    @view_config(route_name='agregar_remolque', request_method='GET',renderer='../templates/agregar_remolque.jinja2')
    def createRegistroRemolques(self):
        try:
            remolque = self.request.dbsession.query(Remolque).all()
        except DBAPIError:
            return Response(db_err_msg, content_type='text/plain', status=500)
        return {'remolques': remolque}


        @view_config(route_name='guardar_remolque', request_method='POST')
        def guardarRegistroImportacion(self):
            try:
                data = self.request.POST
                remolque = Remolque()

                setattr(remolque)
                self.request.dbsession.add(remolque)
                transaction.commit()

            except DBAPIError:
                print('Ocurrio un error al insertar el registro')
                print(db_err_msg)
                # return Response(db_err_msg, content_type='text/plain', status=500)
                return HTTPFound(location='/registro_importacion')
            return HTTPFound(location='/RegistrarVehiculo')



