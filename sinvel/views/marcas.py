import sqlalchemy
import transaction
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from sinvel.models import Marca


class Marcas(object):
    def __init__(self, request):
        self.user = request.user
        self.emp = request.session['grupo']
        self.request = request

    @view_config(route_name='marcaLista', request_method='GET', permission='administrador',
                 renderer='../templates/crud/marca_lista.jinja2')
    def marca_lista(self):
        marcas = self.request.dbsession.query(Marca).all()
        return {'grupo': self.emp, 'user':self.user.user_name, 'marcas': marcas}

    @view_config(route_name='marcaCrear', request_method='GET', permission='administrador',
                 renderer='../templates/crud/marca_create.jinja2')
    def marca_crear(self):
        marca = Marca()
        return {'grupo': self.emp, 'user':self.user.user_name, 'marca': marca}

    @view_config(route_name='marcaCrearGuardar', request_method='POST', permission='administrador')
    def marca_crear_guardar(self):
        data = self.request.POST
        marca = Marca()
        marca.MARCA = data['MARCA']
        self.request.dbsession.add(marca)
        transaction.commit()
        self.request.flash_message.add('Registro Guardado Correctamente!!', message_type='success')
        return HTTPFound(location=self.request.route_url('marcaLista'))

    @view_config(route_name='marcaEditar', request_method='GET', permission='administrador',
                 renderer='../templates/crud/marca_edit.jinja2')
    def marca_editar(self):
        idm = self.request.matchdict['id_marca']
        marka = self.request.dbsession.query(Marca).filter(Marca.ID_MARCA == idm).first()
        return {'grupo': self.emp, 'user':self.user.user_name, 'marka': marka}

    @view_config(route_name='marcaEditarGuardar', request_method='POST', permission='administrador')
    def marca_editar_guardar(self):
        data = self.request.POST
        idm = data['ID_MARCA']
        marka = self.request.dbsession.query(Marca).filter(Marca.ID_MARCA == idm).first()
        for key, value in data.items():
            setattr(marka, key, value)
        transaction.commit()
        self.request.flash_message.add('Registro Guardado Correctamente!!', message_type='success')
        return HTTPFound(location=self.request.route_url('marcaLista'))

    @view_config(route_name='marcaEliminar', request_method='GET', permission='administrador')
    def marca_eliminar(self):
        try:
            idm = self.request.matchdict['id_marca']
            self.request.dbsession.query(Marca).filter(Marca.ID_MARCA == idm).delete()
            transaction.commit()
            self.request.flash_message.add('Registro Eliminado Correctamente!!', message_type='success')
        except sqlalchemy.exc.IntegrityError:
            self.request.flash_message.add('Error al eliminar, existen registros relacionados', message_type='danger')
        return HTTPFound(location=self.request.route_url('marcaLista'))
