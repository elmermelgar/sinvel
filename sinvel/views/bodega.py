import _mysql_exceptions
from pyramid.view import view_config
import transaction
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound
from ..models import Bodega
from ..models import Nivel
from  ..models import Ubicacion
from ..models import Departamento
from ..models import  Vehiculo
from ..models import EstadoVeh
from ..models import DetalleControlEmpresa
from ..models import Venta
from ..models import Cliente
from ..models import Empleado
from ..models import User
from sinvel.views.user import db_err_msg
from ..models import Municipio
from pyramid.httpexceptions import HTTPSeeOther
from sqlalchemy.exc import DBAPIError
from datetime import datetime
import ctypes
from ..models import get_engine

def Mbox(title, text, style):
    ctypes.windll.user32.MessageBoxW(0, text, title, style)

class Bodega_IU(object):
    def __init__(self,request):
        self.request=request
        self.user=request.user.user_name
        self.emp = request.session['grupo']
        self.bodega = Bodega()
        self.nivel = Nivel()
        self.ubicacion = Ubicacion()

    @view_config(route_name='registrarBodega', renderer='../templates/bodega/registrar_bodegas.jinja2',
                 request_method='GET')
    def createRegistroBodega(self):
        try:
            departamentos = self.request.dbsession.query(Departamento).all()
            municipios = self.request.dbsession.query(Municipio).all()

        except DBAPIError:
            return Response(db_err_msg, content_type='text/plain', status=500)
        return {'grupo':self.emp, 'departamentos': departamentos, 'municipios': municipios}

    @view_config(route_name='bodegas', renderer='../templates/bodega/bodegas.jinja2', request_method='GET')
    def bodegas(self):
        items_bodega = self.request.dbsession.query(Bodega).all()
        items_nivel = self.request.dbsession.query(Nivel).all()
        items_ubicacion = self.request.dbsession.query(Ubicacion).all()

        return {'grupo':self.emp, 'bodegas': items_bodega, 'niveles': items_nivel, 'ubicaciones': items_ubicacion,'user':self.user}



    @view_config(route_name='detalle_bodega', renderer='../templates/bodega/detalle_bodega.jinja2', request_method='GET')
    def bodega_detalle(self):
        id = int(self.request.matchdict['id_bod'])
        items_bodega = self.request.dbsession.query(Bodega).get(id)
        items_nivel = self.request.dbsession.query(Nivel).filter_by(ID_BODEGA=items_bodega.ID_BODEGA)
        items_ubicacion = self.request.dbsession.query(Ubicacion).all()


        return {'grupo':self.emp, 'bodega': items_bodega, 'user': self.user, 'niveles': items_nivel, 'ubicaciones': items_ubicacion}

    @view_config(route_name='registroBodegaGuardar', request_method='POST')
    def guardarRegistroBodega(self):
        try:
            data = self.request.POST
            bodega = Bodega()
            for key, value in data.items():
                setattr(bodega, key, value)
            self.request.dbsession.add(bodega)
            transaction.commit()
            ctypes.windll.user32.MessageBoxW(0, "REGISTRO GUARDADO CORRECTAMENTE!!", "EXITO!!", 1)
        except DBAPIError:
            print('Ocurrio un error al insertar el registro')
            print(db_err_msg)
            # return Response(db_err_msg, content_type='text/plain', status=500)
            return HTTPFound(location='/registro_bodega')
        return HTTPFound(location='/bodegas')

    @view_config(route_name='vehiculos', renderer='../templates/bodega/vehiculos.jinja2', request_method='GET')
    def vehiculos(self):
        items_vehiculos = self.request.dbsession.query(Vehiculo).all()

        return {'grupo':self.emp, 'vehiculos': items_vehiculos, 'user': self.user}

    @view_config(route_name='ponerEnVenta', renderer='../templates/bodega/poner_en_venta.jinja2',
                 request_method='GET')
    def poner_en_venta(self):
        id = int(self.request.matchdict['id_veh'])
        items_vehiculo = self.request.dbsession.query(Vehiculo).get(id)
        items_estados = self.request.dbsession.query(EstadoVeh).all()

        return {'grupo':self.emp, 'vehiculo': items_vehiculo, 'user': self.user, 'estados': items_estados}

    @view_config(route_name='ventaVehiculoActualizar', request_method='POST')
    def actualizarVehiculo(self):
        try:
            data = self.request.POST
            id = data.get('ID_VEHICULO')
            vehiculo = self.request.dbsession.query(Vehiculo).get(id)
            veh=vehiculo
            for key, value in data.items():
                if key == 'FOTO_VEH':
                    value = self.request.POST['FOTO_VEH'].file
                    value = value.read()
                setattr(vehiculo, key, value)
            transaction.commit()

        except DBAPIError:
            print('Ocurrio un error al actualizar el registro')
            print(db_err_msg)
            # return Response(db_err_msg, content_type='text/plain', status=500)
            return HTTPFound(location='/vehiculos')
        return HTTPSeeOther(self.request.route_url('asignarVendedor', id_veh=self.request.POST['ID_VEHICULO']))

    @view_config(route_name='asignarVendedor', renderer='../templates/bodega/asignar_vendedor.jinja2',
                 request_method='GET')
    def asignarVendedor(self):
        id = int(self.request.matchdict['id_veh'])
        items_detalle_control = self.request.dbsession.query(DetalleControlEmpresa).filter(DetalleControlEmpresa.ID_VEHICULO==id).filter(DetalleControlEmpresa.TIPO_CONTROL_DET=='Venta').first()
        items_vehiculo = self.request.dbsession.query(Vehiculo).get(id)
        items_venta= self.request.dbsession.query(Venta).filter(Venta.ID_DET_CONTROL==items_detalle_control.ID_DET_CONTROL).first()
        items_empleados = self.request.dbsession.query(Empleado).all()

        return {'grupo':self.emp, 'venta': items_venta, 'user': self.user, 'vehiculo': items_vehiculo, 'empleados': items_empleados}

    @view_config(route_name='actualizarVendedor', request_method='POST')
    def actualizarVendedor(self):
        try:
            data = self.request.POST
            id = data.get('ID_VENTA')
            venta = self.request.dbsession.query(Venta).get(id)

            for key, value in data.items():
                setattr(venta, key, value)
            transaction.commit()

        except DBAPIError:
            print('Ocurrio un error al actualizar el registro')
            print(db_err_msg)
            # return Response(db_err_msg, content_type='text/plain', status=500)
            id = self.request.POST.get('ID_VENTA')
            venta = self.request.dbsession.query(Venta).get(id)
            return HTTPSeeOther(self.request.route_url('resultado', marca=venta.detalle_control_empresa.vehiculo.modelo.marca.ID_MARCA,
                                       modelo=venta.detalle_control_empresa.vehiculo.modelo.ID_MODELO,
                                       estado=venta.detalle_control_empresa.vehiculo.estado_veh.ID_ESTADO,
                                       anio=venta.detalle_control_empresa.vehiculo.ANO))
        id = self.request.POST.get('ID_VENTA')
        venta = self.request.dbsession.query(Venta).get(id)
        return HTTPSeeOther(self.request.route_url('resultado', marca=venta.detalle_control_empresa.vehiculo.modelo.marca.ID_MARCA,
                                                   modelo=venta.detalle_control_empresa.vehiculo.modelo.ID_MODELO,
                                                   estado=venta.detalle_control_empresa.vehiculo.estado_veh.ID_ESTADO,
                                                   anio=venta.detalle_control_empresa.vehiculo.ANO))

    @view_config(route_name='vehiculosAsignados', renderer='../templates/bodega/vehiculos_asignados.jinja2',
                 request_method='GET')
    def vehiculosAsignados(self):
        usuario = self.request.dbsession.query(User).filter(User.user_name==self.user).first()
        items_empleado = self.request.dbsession.query(Empleado).filter(Empleado.ID_USER==usuario.id).first()
        items_ventas = self.request.dbsession.query(Venta).filter(Venta.ID_EMPLEADO==items_empleado.ID_EMPLEADO).all()

        return {'grupo':self.emp, 'user': self.user, 'empleado': items_empleado, 'ventas': items_ventas}

    @view_config(route_name='detalleVehiculo', renderer='../templates/bodega/detalle_vehiculo.jinja2',
                 request_method='GET')
    def detalleVehiculo(self):
        id = int(self.request.matchdict['id_veh'])
        id_ven = int(self.request.matchdict['id_ven'])
        items_vehiculo = self.request.dbsession.query(Vehiculo).get(id)
        items_venta = self.request.dbsession.query(Venta).get(id_ven)
        items_estados = self.request.dbsession.query(EstadoVeh).all()
        filename='sinvel/static/fotos_vehiculos/Vehiculo'+ items_vehiculo.VIN +'.jpg'
        with open(filename, 'wb') as f:
            f.write(items_vehiculo.FOTO_VEH)
        return {'grupo':self.emp, 'vehiculo': items_vehiculo, 'user': self.user, 'estados': items_estados, 'venta': items_venta}

    @view_config(route_name='updateVenta', renderer='../templates/bodega/vender_vehiculo.jinja2',
                 request_method='GET')
    def updateVenta(self):
        id = int(self.request.matchdict['id_veh'])
        id_ven = int(self.request.matchdict['id_ven'])
        items_vehiculo = self.request.dbsession.query(Vehiculo).get(id)
        items_venta = self.request.dbsession.query(Venta).get(id_ven)
        items_clientes= self.request.dbsession.query(Cliente).all()

        return {'grupo':self.emp, 'vehiculo': items_vehiculo, 'user': self.user, 'clientes': items_clientes, 'venta': items_venta}

    @view_config(route_name='actualizarVenta', request_method='POST')
    def actualizarVenta(self):
        try:
            data = self.request.POST
            id_ven = data.get('ID_VENTA')
            id_veh = data.get('ID_VEHICULO')
            dato1 = data.get('PRECIO_VENTA')
            dato2 = data.get('DESCRIP_VENTA')
            dato3 = datetime.strptime(data.get('FECHA_VENTA'), '%d-%m-%Y')
            dato4 = data.get('ID_CLIENTE')

            estadoVeh = self.request.dbsession.query(EstadoVeh).filter(EstadoVeh.COD_ESTADO == '006').one()
            self.request.dbsession.query(Vehiculo).filter(Vehiculo.ID_VEHICULO == id_veh).update(
                {"ID_ESTADO": estadoVeh.ID_ESTADO})

            self.request.dbsession.query(Venta).filter(Venta.ID_VENTA == id_ven).update(
                {"PRECIO_VENTA": dato1, "DESCRIP_VENTA": dato2, "FECHA_VENTA":dato3, "ID_CLIENTE": dato4 })

            transaction.commit()

        except DBAPIError:
            print('Ocurrio un error al actualizar el registro')
            print(db_err_msg)
            # return Response(db_err_msg, content_type='text/plain', status=500)
            return HTTPFound(location='/vehiculos_asignados')
        return HTTPFound(location='/vehiculos_asignados')

    @view_config(route_name='detalleVehiculoCliente', renderer='../templates/bodega/detalle_vehiculo_cliente.jinja2',
                 request_method='GET')
    def detalleVehiculoCliente(self):
        id = int(self.request.matchdict['id_veh'])
        id_ven = int(self.request.matchdict['id_ven'])
        items_vehiculo = self.request.dbsession.query(Vehiculo).get(id)
        items_venta = self.request.dbsession.query(Venta).get(id_ven)
        items_estados = self.request.dbsession.query(EstadoVeh).all()
        filename = 'sinvel/static/fotos_vehiculos/Vehiculo' + items_vehiculo.VIN + '.jpg'
        with open(filename, 'wb') as f:
            f.write(items_vehiculo.FOTO_VEH)
        return {'grupo':self.emp, 'vehiculo': items_vehiculo, 'user': self.user, 'estados': items_estados, 'venta': items_venta}

    @view_config(route_name='vehiculosVendidos', renderer='../templates/bodega/vehiculos_vendidos.jinja2',
                 request_method='GET')
    def vehiculosVendidos(self):
        usuario = self.request.dbsession.query(User).filter(User.user_name == self.user).first()
        items_empleado = self.request.dbsession.query(Empleado).filter(Empleado.ID_USER == usuario.id).first()
        items_ventas = self.request.dbsession.query(Venta).filter(Venta.ID_EMPLEADO == items_empleado.ID_EMPLEADO).all()

        return {'grupo':self.emp, 'user': self.user, 'empleado': items_empleado, 'ventas': items_ventas}

    @view_config(route_name='detalleVenta', renderer='../templates/bodega/detalle_venta.jinja2',
                 request_method='GET')
    def detalleVenta(self):
        id = int(self.request.matchdict['id_veh'])
        id_ven = int(self.request.matchdict['id_ven'])
        items_vehiculo = self.request.dbsession.query(Vehiculo).get(id)
        items_venta = self.request.dbsession.query(Venta).get(id_ven)
        filename = 'sinvel/static/fotos_vehiculos/Vehiculo' + items_vehiculo.VIN + '.jpg'
        with open(filename, 'wb') as f:
            f.write(items_vehiculo.FOTO_VEH)
        return {'grupo':self.emp, 'vehiculo': items_vehiculo, 'user': self.user, 'venta': items_venta}

    @view_config(route_name='guardarNiveles', request_method='POST')
    def guardarNiveles(self):

        settings = {'sqlalchemy.url': 'mysql://root:root@localhost:3306/sinvel'}
        engine = get_engine(settings)
        connection = engine.raw_connection()
        cursor = connection.cursor()

        try:
            data = self.request.POST
            id_bodega = {data.get('ID_BODEGA'),}
            cursor.callproc('sp_crear_niveles', id_bodega)

        except _mysql_exceptions.OperationalError:
            print('Ocurrio un error al insertar el registro')
            ctypes.windll.user32.MessageBoxW(0, "NO PUEDE INGRESAR MAS NIVELES!!", "ERROR!!", 1)
            # return Response(db_err_msg, content_type='text/plain', status=500)
            return HTTPSeeOther(self.request.route_url('detalle_bodega', id_bod=self.request.POST['ID_BODEGA']))
        finally:
            cursor.close()
            connection.commit()
        return HTTPSeeOther(self.request.route_url('detalle_bodega', id_bod=self.request.POST['ID_BODEGA']))

    @view_config(route_name='guardarUbicaciones', request_method='POST')
    def guardarUbicaciones(self):

        settings = {'sqlalchemy.url': 'mysql://root:root@localhost:3306/sinvel'}
        engine = get_engine(settings)
        connection = engine.raw_connection()
        cursor = connection.cursor()

        try:
            data = self.request.POST
            id_bodega = {data.get('ID_BODEGA'), }
            id_nivel = {data.get('ID_NIVEL'), }
            cursor.callproc('sp_crear_ubicacion', id_nivel)

        except _mysql_exceptions.OperationalError:
            print('Ocurrio un error al insertar el registro')
            ctypes.windll.user32.MessageBoxW(0, "NO PUEDE INGRESAR MAS UBICACIONES!!", "ERROR!!", 1)
            # return Response(db_err_msg, content_type='text/plain', status=500)
            return HTTPSeeOther(self.request.route_url('detalle_bodega', id_bod=self.request.POST['ID_BODEGA']))
        finally:
            cursor.close()
            connection.commit()
        return HTTPSeeOther(self.request.route_url('detalle_bodega', id_bod=self.request.POST['ID_BODEGA']))