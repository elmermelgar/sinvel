import time
import transaction
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from sqlalchemy.exc import DBAPIError

from sinvel.models import Vehiculo, EstadoVeh, DetalleControlEmpresa, Reparacion, Costo, TipoCosto
from sinvel.views.user import db_err_msg


class costoReparacion(object):
    def __init__(self,request):
        self.request = request
        self.user = request.user

    @view_config(route_name='costoReparacion',renderer='../templates/costos/costo_reparacion.jinja2',request_method='GET')
    def costoReparacionCreate(self):
        idDce = self.request.matchdict['id_dce']
        dce = self.request.dbsession.query(DetalleControlEmpresa).filter_by(ID_DET_CONTROL=idDce).first()
        reparacion = self.request.dbsession.query(Reparacion).filter_by(ID_DET_CONTROL=idDce).first()
        estados_veh = self.request.dbsession.query(EstadoVeh).all()

        return {'veh':dce.vehiculo, 'estados_veh':estados_veh, 'reparacion':reparacion}

    @view_config(route_name='costoReparacionGuardar', request_method='POST')
    def costoReparacionSave(self):
        try:
            data = self.request.POST
            idDce = data['id_dce']

            #ACTUALIZAR EL COSTO DE LA REPARACION
            self.request.dbsession.query(Reparacion).filter(Reparacion.ID_DET_CONTROL == idDce)\
                .update({"COSTO": data['COSTO'],"ESTADO_REP":data['ESTADO_REP'],'FECHA_REPARACION':time.strftime('%Y-%m-%d')})

            #ACTUALIZAR EL ESTADO DEL VEHICULO
            self.request.dbsession.query(Vehiculo).filter(Vehiculo.ID_VEHICULO == data['idVeh'])\
                .update({"ID_ESTADO": data['ID_ESTADO']})

            #AGREGAR EL NUEVO COSTO A LOS COSTOS DEL VEHICULO
            tcosto = self.request.dbsession.query(TipoCosto).filter(TipoCosto.COD_COSTO=='002').first()
            costo = Costo()
            costo.ID_VEHICULO = data['idVeh']
            costo.ID_TIPO_COSTO = tcosto.ID_TIPO_COSTO
            costo.DESCRIP_COSTO = tcosto.TIPO_COSTO
            costo.MONTO = data['COSTO']
            costo.FECHA_COSTO = time.strftime("%Y-%m-%d")
            self.request.dbsession.add(costo)

            transaction.commit()

        except DBAPIError:
            print('Ocurrio un error al insertar el registro')
            print(db_err_msg)
            return HTTPFound(location='/entrada/costo_reparacion/'+idDce)

        return HTTPFound(location='/entrada/registro_control_entrada_reparacion')