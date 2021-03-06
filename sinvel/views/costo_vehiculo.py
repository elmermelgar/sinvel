from pyramid.view import view_config
from ..models import Costo,User,Vehiculo,TipoCosto,DetalleControlEmpresa,Reparacion
from sqlalchemy.sql import func

class costoVehiculo(object):
    def __init__(self,request):
        self.request = request
        self.user = self.request.user.user_name
        self.emp = request.session['grupo']
        self.item = Costo()
        self.query_costos = request.dbsession.query(Costo)
        self.query_tcostos = request.dbsession.query(TipoCosto)
        self.query_detalleCosto = request.dbsession.query(Vehiculo)


    @view_config(route_name='costo_veh', renderer='../templates/costos/costo_vehiculo.jinja2',request_method='GET')
    def costo_ve (self):
        id_vehiculo=int(self.request.matchdict['id_vehiculo'])
        total=self.request.dbsession.query(func.sum(Costo.MONTO).label('monto')).filter(Costo.ID_VEHICULO==id_vehiculo).scalar()
        costos = self.query_costos.filter(Costo.ID_VEHICULO==id_vehiculo).all()
        vehiculo= self.request.dbsession.query(Vehiculo).get(id_vehiculo)
        return {'grupo':self.emp,'user':self.user, 'costos': costos, 'veh':vehiculo,'total_costo':total}

    @view_config(route_name='detalle_costo', renderer='../templates/costos/detalle_costo.jinja2', request_method='GET')
    def detalle_costo(self):
        id_costo = self.request.matchdict['id_costo']
        costo = self.request.dbsession.query(Costo).\
            filter(Costo.ID_COSTO==id_costo).one()
       # det_cos = self.query_costos.filter(Costo.ID_COSTO == id_costo).one()
        cod_tipo_costo=self.request.dbsession.query(Costo).join(TipoCosto).filter(Costo.ID_COSTO==id_costo)

        if cod_tipo_costo[0].tipo_costo.COD_COSTO=='004':
            det_cos = self.request.dbsession.query(Costo,DetalleControlEmpresa,Reparacion).\
            filter(Costo.ID_VEHICULO==DetalleControlEmpresa.ID_VEHICULO)\
            .filter(DetalleControlEmpresa.ID_DET_CONTROL==Reparacion.ID_DET_CONTROL)\
             .filter(Costo.ID_COSTO==id_costo).one()
            return {'grupo':self.emp,'user':self.user, 'det_cos': det_cos, 'id_vehicu': costo.ID_VEHICULO}
        else:
            return {'grupo':self.emp,'user':self.user, 'det_cos': cod_tipo_costo, 'id_vehicu': costo.ID_VEHICULO}



