from pyramid.response import Response
from pyramid.renderers import render_to_response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.security import NO_PERMISSION_REQUIRED,Authenticated
from ziggurat_foundations.ext.pyramid.sign_in import ZigguratSignInSuccess
from sqlalchemy.exc import DBAPIError
from ..models.models import DetalleImportacion, Importacion
from ..models import get_session_callable
from ..models import ResourceFactory


class Importaciones(object):

    def __init__(self,request):
        self.request=request
        self.user=request.user
        self.item = DetalleImportacion()
        self.query_detalleImp = request.dbsession.query(DetalleImportacion)
        self.query_importacion = request.dbsession.query(Importacion)


    @view_config(route_name='list_importadores', renderer='../templates/importacionFotos/importadores.jinja2', request_method='GET')
    def list(self):
        try:
            detalles = self.query_detalleImp.all()
            importacion = self.query_importacion.all()
        except DBAPIError:
            return Response(db_err_mag, content_type='text/plain', status=500)
        return {'detalle': detalles, 'impor': importacion}
