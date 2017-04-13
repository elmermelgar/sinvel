from pyramid.view import view_config
from ..models.models import DetalleImportacion, Importacion, FotosDesperfecto
from pyramid.httpexceptions import HTTPSeeOther
from pyramid_storage.exceptions import FileNotAllowed
class Importaciones(object):
    def __init__(self,request):
        self.request=request
        self.user=request.user
        self.item = DetalleImportacion()
        self.query_detalleImp = request.dbsession.query(DetalleImportacion)
        self.query_importacion = request.dbsession.query(Importacion)


    @view_config(route_name='list_importadores', renderer='../templates/importacionFotos/importadores.jinja2', request_method='GET')
    def importaciones(self):
            importacion = self.query_importacion.all()

            return {'impor': importacion}

    @view_config(route_name='list_vehiculos', renderer='../templates/importacionFotos/vehiculos.jinja2', request_method='GET')
    def vehiculos(self):
        id_imp=self.request.matchdict['id_imp']
        vehiculos=self.query_detalleImp.filter_by(ID_IMPORTACION =id_imp)

        return {'veh': vehiculos}

    @view_config(route_name='vehiculo', renderer='../templates/importacionFotos/fotosVehiculos.jinja2', request_method='GET')
    def fotos(self):
        id_detImp=self.request.matchdict['id_detImp']
        detImp = self.query_detalleImp.get(id_detImp)

        return {'detImp': detImp }

    @view_config(route_name='subir', request_method='POST')
    def upload(self):
        try:
            foto1=self.request.POST['foto1']
            foto2=self.request.POST['foto2']
            foto3=self.request.POST['foto3']
            foto4=self.request.POST['foto4']
            foto5=self.request.POST['foto5']
            foto6=self.request.POST['foto6']

            detImp=self.request.POST['id_detImp']
            id_veh=self.request.POST['id_veh']
            ob_detImp=self.query_detalleImp.get(detImp)

            foto1.filename=id_veh+'-'+'Bumper.jpg'
            foto2.filename=id_veh+'-'+'Parachoches.jpg'
            foto3.filename=id_veh+'-'+'Costado Izquierdo.jpg'
            foto4.filename=id_veh+'-'+'Costado Derecho.jpg'
            foto5.filename=id_veh+'-'+'tapiceria interna.jpg'
            foto6.filename=id_veh+'-'+'motor.jpg'

            fotos=[foto1, foto2, foto3, foto4, foto5, foto6]

            for foto in fotos:
                if foto is not None:
                    self.request.storage.save(foto, extensions=('jpg', 'png', 'jpeg'))
                    fv=FotosDesperfecto(ID_DETALLE_IMPORT=detImp, FOTO_DESCRIP=foto.filename, FOTO=self.request.storage.base_path+'/'+foto.filename)
                    self.request.dbsession.add(fv)

        except FileNotAllowed:
            self.request.session.flash('Lo sentimos, este archivo no esta Permitido!!!')

        return HTTPSeeOther(self.request.route_url('list_vehiculos', id_imp=ob_detImp.ID_IMPORTACION))

