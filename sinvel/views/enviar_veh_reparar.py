import jsonpickle
import time

import transaction
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from sqlalchemy import func
from sqlalchemy.exc import DBAPIError

from sinvel.models import Taller, TipoReparacion, DetalleControlEmpresa, Reparacion
from sinvel.models.models import Vehiculo, EstadoVeh
from sinvel.views.user import db_err_msg


class RegistroVehiculo(object):
    def __init__(self, request):
        self.emp = request.session['grupo']
        self.request = request
        self.user = request.user

    @view_config(route_name='enviarVehReparar', request_method='GET',
                 renderer='../templates/importador/enviar_reparar.jinja2', permission='importador')
    def enviarVehReparacion(self):
        idVeh = self.request.matchdict['idv']
        veh = self.request.dbsession.query(Vehiculo).filter_by(ID_VEHICULO=idVeh).first()
        items_trep = self.request.dbsession.query(TipoReparacion).all()
        return {'grupo':self.emp, 'user':self.user.user_name, 'items_trep': items_trep, 'veh': veh}

    @view_config(route_name='filterTalleres', request_method='GET', renderer='json', permission='importador')
    def tRepfilterTalleres(self):
        idtrep = self.request.matchdict['idtrep']
        talleres = self.request.dbsession.query(Taller).filter(Taller.ID_TIPO_REPARACION == idtrep).all()
        json_talleres = jsonpickle.encode(talleres, max_depth=2)
        return {'grupo':self.emp, 'json_talleres': json_talleres}

    @view_config(route_name='enviarVehRepararGuardar', request_method='POST', permission='importador')
    def enviarVehRepSave(self):
        try:
            data = self.request.POST
            det_control = DetalleControlEmpresa()
            rep = Reparacion()
            idVeh = data['idVeh']
            veh = self.request.dbsession.query(Vehiculo).filter_by(ID_VEHICULO=idVeh).first()

            det_control.ID_VEHICULO = idVeh
            det_control.TIPO_CONTROL_DET = 'SALREP'

            self.request.dbsession.add(det_control)
            query = self.request.dbsession.query(func.max(DetalleControlEmpresa.ID_DET_CONTROL).label('id_det_control')).filter(DetalleControlEmpresa.TIPO_CONTROL_DET == det_control.TIPO_CONTROL_DET).one()
            iddc = query.id_det_control

            rep.ID_DET_CONTROL = iddc
            rep.ID_TALLER = data['ID_TALLER']
            rep.DESCRIP_REPARACION = data['DESCRIP_REPARACION']

            self.request.dbsession.add(rep)

            # HACER UPDATE DEL ESTADO DEL VEHICULO: A reparar
            estadoVeh = self.request.dbsession.query(EstadoVeh).filter(EstadoVeh.COD_ESTADO == '004').one()
            self.request.dbsession.query(Vehiculo).filter(Vehiculo.ID_VEHICULO == idVeh).update({"ID_ESTADO": estadoVeh.ID_ESTADO})

            transaction.commit()
            self.request.flash_message.add('Registro Guardado Correctamente!!', message_type='success')
        except DBAPIError:
            print('Ocurrio un error al insertar el registro')
            self.request.flash_message.add('Error no se pudo guardar el registro!!', message_type='danger')
            return HTTPFound(location=self.request.route_url('enviarVehReparar', idv=idVeh))

        return HTTPFound(location=self.request.route_url('inicio'))
