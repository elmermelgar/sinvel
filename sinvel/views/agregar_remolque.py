import bcrypt
from pyramid.view import view_config
from ..models import Remolque,User
from sinvel.views.user import db_err_msg
from sqlalchemy.exc import DBAPIError
import transaction
from pyramid.response import Response
from pyramid.view import view_config

from pyramid.httpexceptions import HTTPFound
from sqlalchemy.sql import func


class AgregarRemolque(object):
    def __init__(self,request):
        self.request = request
        self.user = User()

    @view_config(route_name='remolque_list', request_method='GET', renderer='../templates/consultar_remolque.jinja2')
    def remolque_list(self):


        remolque = self.request.dbsession.query(Remolque)

        return {'remolque': remolque}

    @view_config(route_name='agregar_remolque', request_method='GET',renderer='../templates/agregar_remolque.jinja2')
    def createRegistroRemolques(self):
        try:
            remolque = self.request.dbsession.query(Remolque).all()
        except DBAPIError:
            return Response(db_err_msg, content_type='text/plain', status=500)
        return {'remolques': remolque}



    @view_config(route_name='guardar_remolque', request_method='POST')
    def guardarRegistroRemolque(self):
            try:
                data = self.request.POST
                remolque = Remolque()
                remolque.DESCRIP_REMOLQUE=data['DESCRIP_REMOLQUE']
                self.request.dbsession.add(remolque)
                transaction.commit()

            except DBAPIError:
                print('Ocurrio un error al insertar el registro')
                print(db_err_msg)
                return HTTPFound(location='/registro_importacion')
            return HTTPFound(location='/inicio')



