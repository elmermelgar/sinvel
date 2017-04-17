import bcrypt
from pyramid.view import view_config
from ..models import Importador,User
import jsonpickle
from sqlalchemy.exc import DBAPIError
import transaction
from pyramid.httpexceptions import HTTPFound
from sqlalchemy.sql import func
from pyramid_mailer.message import Message

class AgregarImportador(object):
    def __init__(self,request):
        self.request = request
        self.user = User()

    @view_config(route_name='agregar_importador', request_method='GET',renderer='../templates/agregar_importador.jinja2')
    def createimportador(self):
        return {'valor':'0'}

    @view_config(route_name='guardar_importador', request_method='POST')
    def guardarImportador(self):
        try:

            data = self.request.POST
            importador = Importador()
            username=''
            password=''
            user = User()

            for key, value in data.items():
                print(key, value)
                if (key=='CORREO_IMPORTADOR'):
                    user.user_name=value
                    username=value
                    user.email=value
                    user.status=1
                if (key=='NIT'):
                    hashed = bcrypt.hashpw(value.encode('utf-8'), bcrypt.gensalt())
                    user.user_password=hashed
                    password=value

            self.request.dbsession.add(user)
            transaction.commit()
            query = self.request.dbsession.query(func.max(User.id).label('id')).one()
            id = query.id

            for key, value in data.items():
                print(key, value)
                setattr(importador, key, value)
            importador.ID_USER = id
            self.request.dbsession.add(importador)
            transaction.commit()
            mailer = self.request.registry['mailer']
            message = Message(subject="Creacion de Usuario",
                              sender="bd1152017@gmail.com",
                              recipients=[username],
                              body="Es un gusto informarle que su usuario ha sido creado, ya es miembro del grupo de importadores. \n Usuario: " + username +" "+"\nContraseña:"+ password)
            mailer.send_immediately(message, fail_silently=False)

        except DBAPIError:
            return print('Ocurrio un error al insertar el registro')
        return HTTPFound(location='/inicio')




