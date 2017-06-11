import bcrypt
from pyramid.view import view_config
from ..models import Remolque,User,ControlEmpresa,Bodega,Empleado,TipoRemolque
from sinvel.views.user import db_err_msg
from sqlalchemy.exc import DBAPIError

import transaction
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from sqlalchemy.sql import func
from pyramid_flash_message import MessageQueue


class AgregarRemolque(object):
    def __init__(self,request):
        self.request = request
        self.user = self.request.user.user_name
        self.emp = request.session['grupo']

    @view_config(route_name='remolque_list', request_method='GET', renderer='../templates/consultar_remolque.jinja2'
                 ,permission='administrador')
    def remolque_list(self):

        remolque = self.request.dbsession.query(Remolque)
        return {'grupo':self.emp, 'user': self.user, 'remolque': remolque}

    @view_config(route_name='agregar_remolque', request_method='GET',renderer='../templates/agregar_remolque.jinja2',
                 permission='administrador')
    def createRegistroRemolques(self):

        try:
            remolque = self.request.dbsession.query(Remolque).all()
            bodega = self.request.dbsession.query(Bodega).all()
            empleado = self.request.dbsession.query(Empleado).filter(Empleado.TIPO_EMPLEADO=='MOTORISTA').all()
            tipo_remolque = self.request.dbsession.query(TipoRemolque).all()

        except DBAPIError:
            return Response(db_err_msg, content_type='text/plain', status=500)
        return {'grupo':self.emp, 'user': self.user, 'remolque1':remolque,'bodega1': bodega,'empleado1':empleado,'tipo_remolque1':tipo_remolque}



    @view_config(route_name='guardar_remolque', request_method='POST', permission='administrador')
    def guardarRegistroRemolque(self):
            try:
                data = self.request.POST
                remolque = Remolque()
                remolque.DESCRIP_REMOLQUE=data['DESCRIP_REMOLQUE']
                remolque.ID_TIPO_REMOLQUE = data['ID_TIPO_REMOLQUE']
                remolque.ID_BODEGA = data['ID_BODEGA']
                remolque.ID_EMPLEADO = data['ID_EMPLEADO']
                remolque.NOMBRE_REMOLQUE = data['NOMBRE_REMOLQUE']
               
                self.request.dbsession.add(remolque)
                transaction.commit()
                self.request.flash_message.add('Remolque guardado', message_type='success')
            except DBAPIError:
                print('Ocurrio un error al insertar el registro')
                print(db_err_msg)
                return HTTPFound(location='/registro_importacion')
            return HTTPFound(location='/remolque/list')

    @view_config(route_name='delete_remolque', request_method='GET', permission='administrador')
    def deleteRemolque(self):
        id_remolque = self.request.matchdict['id_remolque']
        control=ControlEmpresa()
        control=self.request.dbsession.query(ControlEmpresa).filter(ControlEmpresa.ID_REMOLQUE==id_remolque).count()
        if(control==0):
            self.request.dbsession.query(Remolque).filter(Remolque.ID_REMOLQUE == id_remolque).delete()
            transaction.commit()
            self.request.flash_message.add('Remolque eliminado', message_type='success')
        else:
            self.request.flash_message.add('Error al eliminar', message_type='danger')
            print('no se pudo borrar')
        return HTTPFound(location='/remolque/list')


