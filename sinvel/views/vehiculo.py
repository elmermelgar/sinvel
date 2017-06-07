import jsonpickle
from pyramid.view import view_config
from sqlalchemy import text

from sinvel.models import get_engine
from ..models.models import Marca, EstadoVeh, Vehiculo, Modelo


class Importaciones(object):
    def __init__(self, request):
        self.request=request
        self.user=request.user
        self.query_marca=request.dbsession.query(Marca)
        self.query_estado=request.dbsession.query(EstadoVeh)
        self.query_anio=request.dbsession.query(Vehiculo)
        self.query_modelo=request.dbsession.query(Modelo)

    @view_config(route_name='buscar', renderer='../templates/vehiculo/buscarVehiculo.jinja2', request_method='GET')
    def busqueda(self):
        marca=self.query_marca.all()
        estado=self.query_estado.all()
        anio=self.request.dbsession.execute("select distinct ANO from Vehiculo ORDER BY ANO DESC")

        return {'mar': marca, 'est': estado, 'ani': anio}

    @view_config(route_name='resultado', renderer='../templates/vehiculo/resultadoVehiculo.jinja2', request_method='POST')
    def resultado(self):

        # SQL puro /////////////////////

        settings={'sqlalchemy.url': 'mysql://root:bad@localhost:3306/sinvel'}
        engine=get_engine(settings)
        connection=engine.connect()

        s=text("SELECT * FROM vehiculos where ID_MARCA=:id_marca and ID_MODELO=:id_modelo and ID_ESTADO=:id_estado and ano=:anio")

        veh=connection.execute(s, id_marca=self.request.POST['marca'], id_modelo=self.request.POST['modelo'], id_estado=self.request.POST['estado'], anio=self.request.POST['anio']).fetchall()
        # /////////////////////////////

        return {'veh':veh}

    @view_config(route_name='combo', request_method='GET', renderer='json')
    def all_json_models(self):
        # settings={'sqlalchemy.url': 'mysql://root:bad@localhost:3306/sinvel'}
        # engine=get_engine(settings)
        # connection=engine.raw_connection()
        # cursor=connection.cursor()
        # idmarca=self.request.matchdict['idmarca']
        # args=[int(idmarca), 0, 0]
        # models=cursor.callproc('filtradoModelos', args)
        # cursor.close()
        # connection.commit()
        #
        # print('//////////////////////////////////////')
        # print(models)
        #


        current_brand=self.request.matchdict['idmarca']
        models=self.request.dbsession.query(Modelo).filter(Modelo.ID_MARCA == current_brand).all()
        json_models=jsonpickle.encode(models, max_depth=2)
        return {'json_models': json_models}

    @view_config(route_name='detalle', renderer='../templates/vehiculo/detalleVehiculo.jinja2',request_method='GET')
    def detalle(self):
        id=int(self.request.matchdict['id_veh'])
        veh=self.request.dbsession.query(Vehiculo).get(id)

        return {'vehiculo': veh}
