import time
import transaction
from pyramid.httpexceptions import HTTPFound
from pyramid.tests.pkgs.rendererscanapp import one
from pyramid.view import view_config
from sqlalchemy import func
from sqlalchemy.exc import DBAPIError

from sinvel.models import Bodega, Nivel, Ubicacion
from sinvel.models.models import Empleado, UbicacionBodega
from sinvel.views.user import db_err_msg


class Bodega_IU(object):
    def __init__(self, request):
        self.request = request
        self.emp = request.session['grupo']
        self.user = request.user

    @view_config(route_name='ubiVehSeleccionar', renderer='../templates/ubicar_vehiculo.jinja2',
                 request_method='GET')
    def sel_bodega_ubicacion(self):
        idVeh = self.request.matchdict['idv']
        item_emp = self.request.dbsession.query(Empleado).filter_by(ID_USER=self.user.id).first()
        item_ub = self.request.dbsession.query(UbicacionBodega).filter_by(ID_VEHICULO=idVeh).first()

        items_bodega = item_emp.bodega
        items_nivel = self.request.dbsession.query(Nivel).filter(Nivel.ID_BODEGA==Bodega.ID_BODEGA).filter(Bodega.ID_BODEGA==items_bodega.ID_BODEGA).all()
        items_ubicacion = self.request.dbsession.query(Ubicacion).filter(Ubicacion.ID_NIVEL==Nivel.ID_NIVEL).filter(Nivel.ID_BODEGA==items_bodega.ID_BODEGA).all()

        return {'grupo':self.emp, 'bodega': items_bodega, 'user': self.user, 'niveles': items_nivel, 'ubicaciones': items_ubicacion, 'idVeh':idVeh, 'item_ub':item_ub}

    @view_config(route_name='ubiVehGuardar', request_method='GET')
    def guardarUbicacionVehiculo(self):
        try:
            idUbic = self.request.matchdict['idu']
            idVeh = self.request.matchdict['idv']

            uBodega = UbicacionBodega()

            uBodega.ID_UBICACION = idUbic
            uBodega.ID_VEHICULO = idVeh
            uBodega.FECHAINGRESO = time.strftime("%Y-%m-%d")

            self.request.dbsession.add(uBodega)
            transaction.commit()

        except DBAPIError:
            print('Ocurrio un error al insertar el registro')
            print(db_err_msg)
            # return Response(db_err_msg, content_type='text/plain', status=500)
            return HTTPFound(location='/uv_sel_ubicacion/' + idVeh)
        return HTTPFound(location='/uv_sel_ubicacion/' + idVeh)