from pyramid.view import view_config
from ..models.models import DetalleImportacion, Importacion, Vehiculo, FotosDesperfecto
from pyramid.httpexceptions import HTTPSeeOther
from pyramid_storage.exceptions import FileNotAllowed
import transaction

class Importaciones(object):
    def __init__(self,request):
        self.request=request
        self.user=request.user
        self.item = DetalleImportacion()
        self.query_detalleImp = request.dbsession.query(DetalleImportacion)
        self.query_importacion = request.dbsession.query(Importacion)
        self.query_vehiculo = request.dbsession.query(Vehiculo)


    @view_config(route_name='list_importadores', renderer='../templates/importacionFotos/importadores.jinja2', request_method='GET')
    def importaciones(self):
            importacion = self.query_importacion.all()

            return {'impor': importacion}

    @view_config(route_name='list_vehiculos', renderer='../templates/importacionFotos/vehiculos.jinja2', request_method='GET')
    def vehiculos(self):
        id_det=self.request.matchdict['id_imp']
        vehiculos=self.query_detalleImp.filter_by(ID_IMPORTACION =id_det)

        return {'veh': vehiculos}

    @view_config(route_name='vehiculo', renderer='../templates/importacionFotos/fotosVehiculos.jinja2', request_method='GET')
    def fotos(self):
        id = self.request.matchdict['id_veh']
        imp = self.request.matchdict['id_imp']
        vehiculo = self.query_vehiculo.get(id)

        return {'veh': vehiculo, 'imp': imp}

    @view_config(route_name='subir', request_method='POST')
    def upload(self):
        try:
            foto1=self.request.POST['foto1']
            foto2=self.request.POST['foto2']
            foto3=self.request.POST['foto3']
            foto4=self.request.POST['foto4']
            foto5=self.request.POST['foto5']
            foto6=self.request.POST['foto6']
            fotos=[foto1,foto2,foto3,foto4,foto5,foto6]

            id_imp=self.request.POST['id_imp']
            detImp=self.query_detalleImp.filter_by(ID_IMPORTACION=id_imp)
            detImp2=detImp.ID_DETALLE_IMPORT

            for foto in fotos:
                if foto is not None:
                    self.request.storage.save(foto, extensions=('jpg', 'png', 'jpeg'))
                    fv=FotosDesperfecto(ID_DETALLE_IMPORT=detImp2, FOTO_DESCRIP="b", FOTO="a")
                    self.request.dbsession.add(fv)

        except FileNotAllowed:
            self.request.session.flash('Lo sentimos, este archivo no esta Permitido!!!')


        return HTTPSeeOther(self.request.route_url('list_vehiculos', id_imp=id_imp))

