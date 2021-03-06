from pyramid.view import view_config
from ..models.models import User, Empleado, Bodega, DetalleControlEmpresa, \
    Vehiculo, DetalleImportacion, Importacion, FotosDesperfecto, Ubicacion, UbicacionBodega
from pyramid.httpexceptions import HTTPSeeOther
from pyramid_storage.exceptions import FileNotAllowed


class Importaciones(object):
    def __init__(self, request):
        self.request = request
        self.user_name = self.request.user.user_name
        self.emp = request.session['grupo']
        self.user = request.user.id
        self.query_emp = request.dbsession.query(Empleado)
        self.query_bodega = request.dbsession.query(Bodega)
        self.query_detalleCtl = request.dbsession.query(DetalleControlEmpresa)
        self.query_veh = request.dbsession.query(Vehiculo)
        self.query_detalleImp = request.dbsession.query(DetalleImportacion)
        self.query_importacion = request.dbsession.query(Importacion)
        self.query_foto = request.dbsession.query(FotosDesperfecto)

    @view_config(route_name='list_importadores', renderer='../templates/importacionFotos/importadores.jinja2',
                 request_method='GET', permission='bodeguero')
    def importaciones(self):
        emp = self.request.dbsession.query(Empleado).filter(Empleado.ID_USER==self.user).first()
        subquery = self.request.dbsession.query(UbicacionBodega.ID_VEHICULO)
        det_imp = self.request.dbsession.query(DetalleImportacion) \
            .filter(DetalleImportacion.ID_IMPORTACION == Importacion.ID_IMPORTACION) \
            .filter(Importacion.ID_BODEGA == emp.ID_BODEGA) \
            .filter(DetalleControlEmpresa.ID_EMPLEADO!=None)\
            .filter(DetalleControlEmpresa.ID_VEHICULO==DetalleImportacion.ID_VEHICULO)\
            .filter(DetalleControlEmpresa.TIPO_CONTROL_DET=='ENTRA')\
            .filter(DetalleImportacion.ID_VEHICULO.notin_(subquery)).all()

        return {'grupo': self.emp, 'user': self.user_name, 'emp': emp, 'det_imp': det_imp}


    @view_config(route_name='vehiculo', renderer='../templates/importacionFotos/fotosVehiculos.jinja2',
                 request_method='GET', permission='bodeguero')
    def fotos(self):
        id_detImp = self.request.matchdict['id_detImp']
        detImp = self.query_detalleImp.get(id_detImp)

        return {'grupo': self.emp, 'detImp': detImp}


    @view_config(route_name='subir', request_method='POST', permission='bodeguero')
    def upload(self):
        try:
            foto1 = self.request.POST['foto1']
            foto2 = self.request.POST['foto2']
            foto3 = self.request.POST['foto3']
            foto4 = self.request.POST['foto4']
            foto5 = self.request.POST['foto5']
            foto6 = self.request.POST['foto6']

            detImp = self.request.POST['id_detImp']
            id_veh = self.request.POST['id_veh']
            ob_detImp = self.query_detalleImp.get(detImp)

            foto1.filename = id_veh + '-' + 'Bumper.jpg'
            foto2.filename = id_veh + '-' + 'Parachoches.jpg'
            foto3.filename = id_veh + '-' + 'Costado Izquierdo.jpg'
            foto4.filename = id_veh + '-' + 'Costado Derecho.jpg'
            foto5.filename = id_veh + '-' + 'tapiceria interna.jpg'
            foto6.filename = id_veh + '-' + 'motor.jpg'

            fotos = [foto1, foto2, foto3, foto4, foto5, foto6]

            for foto in fotos:
                if foto is not None:
                    self.request.storage.save(foto, extensions=('jpg', 'png', 'jpeg'))
                    fv = FotosDesperfecto(ID_DETALLE_IMPORT=detImp, FOTO_DESCRIP=foto.filename,
                                          FOTO=self.request.storage.base_path + '/' + foto.filename)
                    self.request.dbsession.add(fv)

            self.request.flash_message.add('Fotos Subidas con Exito!!', message_type='success')

        except FileNotAllowed:
            self.request.flash_message.add('Lo sentimos, este archivo no esta Permitido!!!', message_type='danger')

        return HTTPSeeOther(self.request.route_url('list_importadores'))
