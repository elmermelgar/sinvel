import transaction
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from sinvel.models import Cliente


class Clientes(object):
    def __init__(self, request):
        self.user = request.user
        self.emp = request.session['grupo']
        self.request = request

    @view_config(route_name='clienteLista', request_method='GET', permission='administrador',
                 renderer='../templates/crud/cliente_lista.jinja2')
    def cliente_lista(self):
        clientes = self.request.dbsession.query(Cliente).all()
        return {'grupo': self.emp, 'user':self.user.user_name, 'clientes': clientes}

    @view_config(route_name='clienteCrear', request_method='GET', permission='administrador',
                 renderer='../templates/crud/cliente_create.jinja2')
    def cliente_crear(self):
        cliente = Cliente()
        return {'grupo': self.emp, 'user':self.user.user_name, 'cliente': cliente}

    @view_config(route_name='clienteCrearGuardar', request_method='POST', permission='administrador')
    def cliente_crear_guardar(self):
        data = self.request.POST
        cliente = Cliente()
        cliente.NOMBRE_CLIENTE = data['NOMBRE_CLIENTE']
        cliente.APELLIDO_CLIENTE = data['APELLIDO_CLIENTE']
        cliente.FECHA_NACIMIENTO = data['FECHA_NACIMIENTO']
        cliente.SEXO = data['SEXO']
        cliente.DUI = data['DUI']
        self.request.dbsession.add(cliente)
        transaction.commit()
        self.request.flash_message.add('Registro Guardado Correctamente!!', message_type='success')
        return HTTPFound(location=self.request.route_url('clienteLista'))

    @view_config(route_name='clienteEditar', request_method='GET', permission='administrador',
                 renderer='../templates/crud/cliente_edit.jinja2')
    def cliente_editar(self):
        idc = self.request.matchdict['id_cliente']
        cliente = self.request.dbsession.query(Cliente).filter(Cliente.ID_CLIENTE == idc).first()
        return {'grupo': self.emp, 'user':self.user.user_name, 'cliente': cliente}

    @view_config(route_name='clienteEditarGuardar', request_method='POST', permission='administrador')
    def cliente_editar_guardar(self):
        data = self.request.POST
        idc = data['ID_CLIENTE']
        cliente = self.request.dbsession.query(Cliente).filter(Cliente.ID_CLIENTE == idc).first()
        for key, value in data.items():
            setattr(cliente, key, value)
        transaction.commit()
        self.request.flash_message.add('Registro Guardado Correctamente!!', message_type='success')
        return HTTPFound(location=self.request.route_url('clienteLista'))

    @view_config(route_name='clienteEliminar', request_method='GET', permission='administrador')
    def cliente_eliminar(self):
        idc = self.request.matchdict['id_cliente']
        self.request.dbsession.query(Cliente).filter(Cliente.ID_CLIENTE == idc).delete()
        transaction.commit()
        self.request.flash_message.add('Registro Eliminado Correctamente!!', message_type='success')
        return HTTPFound(location=self.request.route_url('clienteLista'))
