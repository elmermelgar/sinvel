import sqlalchemy
import transaction
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from sinvel.models import Modelo, Marca


class Modelos(object):
    def __init__(self, request):
        self.user = request.user
        self.emp = request.session['grupo']
        self.request = request

    @view_config(route_name='modeloLista', request_method='GET', permission='administrador',
                 renderer='../templates/crud/modelo_lista.jinja2')
    def modelo_lista(self):
        modelos = self.request.dbsession.query(Modelo,Marca)\
            .join(Marca).order_by(Marca.MARCA).all()
        return {'grupo': self.emp, 'user':self.user.user_name, 'modelos': modelos}

    @view_config(route_name='modeloCrear', request_method='GET', permission='administrador',
                 renderer='../templates/crud/modelo_create.jinja2')
    def modelo_crear(self):
        markas = self.request.dbsession.query(Marca).order_by(Marca.MARCA).all()
        return {'grupo': self.emp, 'user':self.user.user_name, 'markas': markas}

    @view_config(route_name='modeloCrearGuardar', request_method='POST', permission='administrador')
    def modelo_crear_guardar(self):
        data = self.request.POST
        model = Modelo()
        model.ID_MARCA = data['ID_MARCA']
        model.MODELO = data['MODELO']
        self.request.dbsession.add(model)
        transaction.commit()
        self.request.flash_message.add('Registro Guardado Correctamente!!', message_type='success')
        return HTTPFound(location=self.request.route_url('modeloLista'))

    @view_config(route_name='modeloEditar', request_method='GET', permission='administrador',
                 renderer='../templates/crud/modelo_edit.jinja2')
    def modelo_editar(self):
        idm = self.request.matchdict['id_modelo']
        model = self.request.dbsession.query(Modelo).filter(Modelo.ID_MODELO == idm).first()
        markas = self.request.dbsession.query(Marca).order_by(Marca.MARCA).all()
        return {'grupo': self.emp, 'user':self.user.user_name, 'model': model, 'markas': markas}

    @view_config(route_name='modeloEditarGuardar', request_method='POST', permission='administrador')
    def modelo_editar_guardar(self):
        data = self.request.POST
        idm = data['ID_MODELO']
        model = self.request.dbsession.query(Modelo).filter(Modelo.ID_MODELO == idm).first()
        for key, value in data.items():
            setattr(model, key, value)
        transaction.commit()
        self.request.flash_message.add('Registro Guardado Correctamente!!', message_type='success')
        return HTTPFound(location=self.request.route_url('modeloLista'))

    @view_config(route_name='modeloEliminar', request_method='GET', permission='administrador')
    def modelo_eliminar(self):
        try:
            idm = self.request.matchdict['id_modelo']
            self.request.dbsession.query(Modelo).filter(Modelo.ID_MODELO == idm).delete()
            transaction.commit()
            self.request.flash_message.add('Registro Eliminado Correctamente!!', message_type='success')
        except sqlalchemy.exc.IntegrityError:
            self.request.flash_message.add('Error al eliminar, existen registros relacionados', message_type='danger')
        return HTTPFound(location=self.request.route_url('modeloLista'))
