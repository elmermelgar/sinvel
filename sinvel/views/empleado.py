import bcrypt
from sqlalchemy import exc
from pyramid.view import view_config
from pyramid.renderers import render_to_response
from sinvel.models import Importador,User,Empleado,Group,UsersGroup,Bodega
from sqlalchemy.exc import DBAPIError
import transaction
from pyramid.httpexceptions import HTTPFound
from sqlalchemy.sql import func
from pyramid_mailer.message import Message
from pyramid.view import forbidden_view_config
from pyramid.response import Response
from pyramid.security import (
    ALL_PERMISSIONS,
    Allow,
    unauthenticated_userid,
    Everyone,
    Authenticated
    )

class EmpleadoClase(object):
    def __init__(self,request):

        self.emp = request.session['grupo']
        self.request = request
        self.user = request.user

    @view_config(route_name='empleado_list', renderer='../templates/crud/empleado.jinja2',
                 request_method='GET',permission='administrador')
    def listEmpleado(self):

        usuario = self.request.dbsession.query(User).filter(User.user_name == self.user.user_name).first()
        empleado = self.request.dbsession.query(Empleado).filter(Empleado.ID_USER == usuario.id).first()
        empleados = self.request.dbsession.query(Empleado).filter(Empleado.ID_BODEGA == empleado.ID_BODEGA).all()

        return {'grupo':self.emp, 'empleados': empleados}

    @view_config(route_name='empleado_create', request_method='GET', renderer='../templates/crud/empleado_create.jinja2',permission='administrador')
    def createEmpleado(self):
        bodegas = None
        try:
            bodegas = self.request.dbsession.query(Bodega).all()
        except:
            print('Error')
        return {'grupo':self.emp, 'bodegas':bodegas}



    @view_config(route_name='guardar_empleado', request_method='POST')
    def guardarEmpleado(self):
        usuario = self.request.dbsession.query(User).filter(User.user_name == self.user.user_name).first()
        bodega = self.request.dbsession.query(Empleado).filter(Empleado.ID_USER == usuario.id).first()

        try:

            data = self.request.POST
            empleado = Empleado()
            username = ''
            password = ''
            user = User()
            grupo=UsersGroup()
            grupoUser=Group()
            email=''
            nameGroup=''
            idUser=''

            if (data['TIPO_EMPLEADO'] != 'MOTORISTA'):
                for key, value in data.items():
                    print(key, value)
                    if (key == 'email'):
                        user.user_name = data['username']
                        username = data['username']
                        user.email = value
                        user.status = 1
                    email=user.email
                    if (key == 'NIT'):
                        hashed = bcrypt.hashpw(value.encode('utf-8'), bcrypt.gensalt())
                        user.user_password = hashed
                        password = value
                self.request.dbsession.add(user)
                query = self.request.dbsession.query(func.max(User.id).label('id')).one()

                id = query.id
                grupoUser=self.request.dbsession.query(Group).filter(Group.description==data['TIPO_EMPLEADO']).first()
                nameGroup=grupoUser.group_name
                grupo.group_id=grupoUser.id
                grupo.user_id=id
                idUser=id
                self.request.dbsession.add(grupo)

            if (data['TIPO_EMPLEADO'] != 'MOTORISTA'):
             for key, value in data.items():
                print(key, value)
                setattr(empleado, key, value)
                empleado.ID_USER = idUser
                #empleado.ID_BODEGA = bodega.ID_BODEGA
            else:
                for key, value in data.items():
                    print(key, value)
                    setattr(empleado, key, value)

            self.request.dbsession.add(empleado)
            transaction.commit()
            self.request.dbsession.close()
            self.request.flash_message.add('Empleado guardado', message_type='success')
            if (data['TIPO_EMPLEADO'] != 'MOTORISTA'):
                mailer = self.request.registry['mailer']
                message = Message(subject="Creacion de Usuario",
                              sender="bd1152017@gmail.com",
                              recipients=[email],
                              body="Es un gusto informarle que su usuario ha sido creado, ya es miembro del grupo de "+nameGroup+". \n Usuario: " + username + " " + "\nContraseña:" + password)
                mailer.send_immediately(message, fail_silently=False)

        except DBAPIError:
            return print('Ocurrio un error al insertar el registro')
        #values = self.listEmpleado(self.request)
        #renderer = values['']
        #return render_to_response(renderer, values)
        return HTTPFound(location='/empleado/list')


    @view_config(route_name='empleado_delete', request_method='GET',permission='administrador')
    def deleteEmpleado(self):

      try:
            id_empleado = self.request.matchdict['id_empleado']
            print(id_empleado)
            usuario = self.request.dbsession.query(User).filter(User.user_name == self.user.user_name).first()
            empleado = self.request.dbsession.query(Empleado).filter(Empleado.ID_EMPLEADO==id_empleado).first()
            self.request.dbsession.query(Empleado).filter(Empleado.ID_EMPLEADO == empleado.ID_EMPLEADO).delete()
            transaction.commit()
            self.request.dbsession.query(User).filter(User.id == empleado.ID_USER).delete()
            transaction.commit()
            self.request.flash_message.add('Empleado elminado', message_type='success')
            return HTTPFound(location='/empleado/list')

      except exc.IntegrityError as e:
            #self.request.session().rollback()
            self.request.flash_message.add('Error al eliminar por integridad referencial', message_type='danger')
            return HTTPFound(location='/empleado/list')
