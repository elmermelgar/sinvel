# coding: utf-8
from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, Numeric, SmallInteger, String, Text, Time
from sqlalchemy.orm import relationship
from sqlalchemy.schema import FetchedValue
from sqlalchemy.dialects.mysql.types import LONGBLOB
from sqlalchemy.ext.declarative import declarative_base



Base = declarative_base()
metadata = Base.metadata


class AlembicZigguratFoundationsVersion(Base):
    __tablename__ = 'alembic_ziggurat_foundations_version'

    version_num = Column(String(32), primary_key=True)


class Bodega(Base):
    __tablename__ = 'bodega'

    ID_BODEGA = Column(Integer, primary_key=True)
    ID_MUNICIPIO = Column(ForeignKey('municipio.ID_MUNICIPIO'), ForeignKey('municipio.ID_MUNICIPIO'), index=True)
    NOMBRE_BODEGA = Column(String(50))
    DESCRIPCION_BODEGA = Column(String(200))
    DIRECCION_BODEGA = Column(String(200))


    municipio = relationship('Municipio', primaryjoin='Bodega.ID_MUNICIPIO == Municipio.ID_MUNICIPIO', backref='municipio_bodegas')
    municipio1 = relationship('Municipio', primaryjoin='Bodega.ID_MUNICIPIO == Municipio.ID_MUNICIPIO', backref='municipio_bodegas_0')


class Cliente(Base):
    __tablename__ = 'cliente'

    ID_CLIENTE = Column(Integer, primary_key=True)
    ID = Column(ForeignKey('users.id'), ForeignKey('users.id'), index=True)
    NOMBRE_CLIENTE = Column(String(50))
    APELLIDO_CLIENTE = Column(String(50))
    FECHA_NACIMIENTO = Column(Date)
    SEXO = Column(String(1))
    DUI = Column(String(9))

    user = relationship('User', primaryjoin='Cliente.ID == User.id', backref='user_clientes')
    user1 = relationship('User', primaryjoin='Cliente.ID == User.id', backref='user_clientes_0')


class ControlEmpresa(Base):
    __tablename__ = 'control_empresa'

    ID_CONTROL = Column(Integer, primary_key=True)
    ID_REMOLQUE = Column(ForeignKey('remolque.ID_REMOLQUE'), index=True)
    TIPO_CONTROL = Column(String(20))
    DESCRIPCION_CONTROL = Column(String(200))
    HORA_CONTROL = Column(Time)
    FECHA_CONTROL = Column(Date)

    remolque = relationship('Remolque', primaryjoin='ControlEmpresa.ID_REMOLQUE == Remolque.ID_REMOLQUE', backref='control_empresas')


class Costo(Base):
    __tablename__ = 'costo'

    ID_COSTO = Column(Integer, primary_key=True)
    ID_TIPO_COSTO = Column(ForeignKey('tipo_costo.ID_TIPO_COSTO'), index=True)
    ID_VEHICULO = Column(ForeignKey('vehiculo.ID_VEHICULO'), index=True)
    DESCRIP_COSTO = Column(String(100))
    MONTO = Column(Numeric(10, 2))

    tipo_costo = relationship('TipoCosto', primaryjoin='Costo.ID_TIPO_COSTO == TipoCosto.ID_TIPO_COSTO', backref='costoes')
    vehiculo = relationship('Vehiculo', primaryjoin='Costo.ID_VEHICULO == Vehiculo.ID_VEHICULO', backref='costoes')


class CostosBodega(Base):
    __tablename__ = 'costos_bodega'

    ID_COSTO_BOD = Column(Integer, primary_key=True)
    ID_BODEGA = Column(ForeignKey('bodega.ID_BODEGA'), index=True)
    COSTO_POR_DIA = Column(Numeric(10, 2))
    MULTA = Column(Numeric(10, 2))

    bodega = relationship('Bodega', primaryjoin='CostosBodega.ID_BODEGA == Bodega.ID_BODEGA', backref='costos_bodegas')


class Departamento(Base):
    __tablename__ = 'departamento'

    ID_DEPARTAMENTO = Column(Integer, primary_key=True)
    COD_DEPARTAMENTO = Column(String(10))
    DEPARTAMENTO = Column(String(100))


class DetalleControlEmpresa(Base):
    __tablename__ = 'detalle_control_empresa'

    ID_DET_CONTROL = Column(Integer, primary_key=True)
    ID_CONTROL = Column(ForeignKey('control_empresa.ID_CONTROL'), index=True)
    ID_EMPLEADO = Column(ForeignKey('empleado.ID_EMPLEADO'), index=True)
    ID_VEHICULO = Column(ForeignKey('vehiculo.ID_VEHICULO'), index=True)
    TIPO_CONTROL_DET=Column(String(20))
    control_empresa = relationship('ControlEmpresa', primaryjoin='DetalleControlEmpresa.ID_CONTROL == ControlEmpresa.ID_CONTROL', backref='detalle_control_empresas')
    empleado = relationship('Empleado', primaryjoin='DetalleControlEmpresa.ID_EMPLEADO == Empleado.ID_EMPLEADO', backref='detalle_control_empresas')
    vehiculo = relationship('Vehiculo', primaryjoin='DetalleControlEmpresa.ID_VEHICULO == Vehiculo.ID_VEHICULO', backref='detalle_control_empresas')


class DetalleImportacion(Base):
    __tablename__ = 'detalle_importacion'

    ID_DETALLE_IMPORT = Column(Integer, primary_key=True)
    ID_VEHICULO = Column(ForeignKey('vehiculo.ID_VEHICULO'), index=True)
    ID_IMPORTACION = Column(ForeignKey('importacion.ID_IMPORTACION'), ForeignKey('importacion.ID_IMPORTACION'), index=True)
    DETALLE_DESPERFECTO = Column(String(400))
    ADUANA = Column(String(100))

    importacion = relationship('Importacion', primaryjoin='DetalleImportacion.ID_IMPORTACION == Importacion.ID_IMPORTACION', backref='importacion_detalle_importacions')
    importacion1 = relationship('Importacion', primaryjoin='DetalleImportacion.ID_IMPORTACION == Importacion.ID_IMPORTACION', backref='importacion_detalle_importacions_0')
    vehiculo = relationship('Vehiculo', primaryjoin='DetalleImportacion.ID_VEHICULO == Vehiculo.ID_VEHICULO', backref='detalle_importacions')


class Empleado(Base):
    __tablename__ = 'empleado'

    ID_EMPLEADO = Column(Integer, primary_key=True)
    ID_BODEGA = Column(ForeignKey('bodega.ID_BODEGA'), index=True)
    ID_USER = Column(ForeignKey('users.id'), index=True)
    NOMBRE = Column(String(50))
    APELLIDO = Column(String(50))
    GENERO = Column(String(20))
    FECHA_NACIMIENTO = Column(Date)
    NIT = Column(String(18))
    DUI = Column(String(9))
    AFP = Column(String(18))
    ISSS = Column(String(18))
    TEL_EMP = Column(String(9))

    bodega = relationship('Bodega', primaryjoin='Empleado.ID_BODEGA == Bodega.ID_BODEGA', backref='empleadoes')
    user = relationship('User', primaryjoin='Empleado.ID_USER == User.id', backref='empleadoes')


class EstadoVeh(Base):
    __tablename__ = 'estado_veh'

    ID_ESTADO = Column(Integer, primary_key=True)
    ESTADO = Column(String(50))
    DESCRIP_ESTADO = Column(String(200))


class ExternalIdentity(Base):
    __tablename__ = 'external_identities'

    external_id = Column(String(255), primary_key=True, nullable=False)
    external_user_name = Column(String(255))
    provider_name = Column(String(50), primary_key=True, nullable=False)
    access_token = Column(String(512))
    alt_token = Column(String(512))
    token_secret = Column(String(512))
    local_user_id = Column(ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)

    local_user = relationship('User', primaryjoin='ExternalIdentity.local_user_id == User.id', backref='external_identities')


class FotosDesperfecto(Base):
    __tablename__ = 'fotos_desperfecto'

    ID_FOTOS = Column(Integer, primary_key=True)
    ID_DETALLE_IMPORT = Column(ForeignKey('detalle_importacion.ID_DETALLE_IMPORT'), index=True)
    FOTO_DESCRIP = Column(String(200))
    FOTO = Column(String(200))

    detalle_importacion = relationship('DetalleImportacion', primaryjoin='FotosDesperfecto.ID_DETALLE_IMPORT == DetalleImportacion.ID_DETALLE_IMPORT', backref='fotos_desperfectoes')


class Group(Base):
    __tablename__ = 'groups'

    group_name = Column(String(128), nullable=False, unique=True)
    description = Column(Text)
    member_count = Column(Integer, nullable=False)
    id = Column(Integer, primary_key=True)


class GroupsPermission(Base):
    __tablename__ = 'groups_permissions'

    perm_name = Column(String(64), primary_key=True, nullable=False)
    group_id = Column(ForeignKey('groups.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)

    group = relationship('Group', primaryjoin='GroupsPermission.group_id == Group.id', backref='groups_permissions')


class GroupsResourcesPermission(Base):
    __tablename__ = 'groups_resources_permissions'

    resource_id = Column(ForeignKey('resources.resource_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    perm_name = Column(String(64), primary_key=True, nullable=False)
    group_id = Column(ForeignKey('groups.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)

    group = relationship('Group', primaryjoin='GroupsResourcesPermission.group_id == Group.id', backref='groups_resources_permissions')
    resource = relationship('Resource', primaryjoin='GroupsResourcesPermission.resource_id == Resource.resource_id', backref='groups_resources_permissions')


class Importacion(Base):
    __tablename__ = 'importacion'

    ID_IMPORTACION = Column(Integer, primary_key=True)
    ID_IMPORTADOR = Column(ForeignKey('importador.ID_IMPORTADOR'), index=True)
    NUM_REGISTRO = Column(Integer)
    FECHA_IMP = Column(Date)
    PESO = Column(Numeric(10, 2))
    VALOR_ADUANERO = Column(Numeric(10, 2))
    VALOR_FACTURADO = Column(Numeric(10, 2))
    PAIS_ORIGEN = Column(String(50))

    importador = relationship('Importador', primaryjoin='Importacion.ID_IMPORTADOR == Importador.ID_IMPORTADOR', backref='importacions')


class Importador(Base):
    __tablename__ = 'importador'

    ID_IMPORTADOR = Column(Integer, primary_key=True)
    ID_USER = Column(ForeignKey('users.id'), index=True)
    NOMBRE = Column(String(50))
    APELLIDO = Column(String(50))
    GENERO = Column(String(20))
    FECHA_NACIMIENTO = Column(Date)
    TELEFONO_CASA = Column(String(9))
    TELEFONO_CELULAR = Column(String(9))
    CORREO_IMPORTADOR = Column(String(60))
    RESPONSABLE = Column(String(100))
    NIT = Column(String(18))
    DUI = Column(String(10))
    APELLIDO_CASADA = Column(String(40))

    user = relationship('User', primaryjoin='Importador.ID_USER == User.id', backref='importadors')


class ImportadorTaller(Base):
    __tablename__ = 'importador_taller'

    ID_IMPORTADOR_TALLER = Column(Integer, primary_key=True)
    ID_TALLER = Column(ForeignKey('taller.ID_TALLER'), index=True)
    ID_IMPORTADOR = Column(ForeignKey('importador.ID_IMPORTADOR'), index=True)

    importador = relationship('Importador', primaryjoin='ImportadorTaller.ID_IMPORTADOR == Importador.ID_IMPORTADOR', backref='importador_tallers')
    taller = relationship('Taller', primaryjoin='ImportadorTaller.ID_TALLER == Taller.ID_TALLER', backref='importador_tallers')


class Marca(Base):
    __tablename__ = 'marca'

    ID_MARCA = Column(Integer, primary_key=True)
    MARCA = Column(String(100))


class Modelo(Base):
    __tablename__ = 'modelo'

    ID_MODELO = Column(Integer, primary_key=True)
    MODELO = Column(String(100))
    ID_MARCA = Column(ForeignKey('marca.ID_MARCA'), ForeignKey('marca.ID_MARCA'), nullable=False, index=True)


    marca = relationship('Marca', primaryjoin='Modelo.ID_MARCA == Marca.ID_MARCA', backref='marca_modeloes')
    marca1 = relationship('Marca', primaryjoin='Modelo.ID_MARCA == Marca.ID_MARCA', backref='marca_modeloes_0')


class Model(Base):
    __tablename__ = 'models'

    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)
    value = Column(Integer)


class Municipio(Base):
    __tablename__ = 'municipio'

    ID_MUNICIPIO = Column(Integer, primary_key=True)
    ID_DEPARTAMENTO = Column(ForeignKey('departamento.ID_DEPARTAMENTO'), ForeignKey('departamento.ID_DEPARTAMENTO'), index=True)
    COD_MUNICIPIO = Column(String(10))
    MUNICIPIO = Column(String(100))

    departamento = relationship('Departamento', primaryjoin='Municipio.ID_DEPARTAMENTO == Departamento.ID_DEPARTAMENTO', backref='departamento_municipios')
    departamento1 = relationship('Departamento', primaryjoin='Municipio.ID_DEPARTAMENTO == Departamento.ID_DEPARTAMENTO', backref='departamento_municipios_0')


class Nivel(Base):
    __tablename__ = 'nivel'

    ID_NIVEL = Column(Integer, primary_key=True)
    ID_BODEGA = Column(ForeignKey('bodega.ID_BODEGA'), index=True)
    DESCRIPCION_NIVEL = Column(String(50))
    CANTIDAD_DISP = Column(Integer)
    CANTIDAD_MAX = Column(Integer)

    bodega = relationship('Bodega', primaryjoin='Nivel.ID_BODEGA == Bodega.ID_BODEGA', backref='nivels')


class Remolque(Base):
    __tablename__ = 'remolque'

    ID_REMOLQUE = Column(Integer, primary_key=True)
    ID_TIPO_REMOLQUE = Column(ForeignKey('tipo_remolque.ID_TIPO_REMOLQUE'), index=True)
    ID_BODEGA = Column(ForeignKey('bodega.ID_BODEGA'), index=True)
    ID_EMPLEADO = Column(ForeignKey('empleado.ID_EMPLEADO'), index=True)
    DESCRIP_REMOLQUE = Column(String(200))
    NOMBRE_REMOLQUE = Column(String(100))
    DISPONIBLE = Column(Integer)

    bodega = relationship('Bodega', primaryjoin='Remolque.ID_BODEGA == Bodega.ID_BODEGA', backref='remolques')
    empleado = relationship('Empleado', primaryjoin='Remolque.ID_EMPLEADO == Empleado.ID_EMPLEADO', backref='remolques')
    tipo_remolque = relationship('TipoRemolque', primaryjoin='Remolque.ID_TIPO_REMOLQUE == TipoRemolque.ID_TIPO_REMOLQUE', backref='remolques',lazy="joined", innerjoin=True)


class Reparacion(Base):
    __tablename__ = 'reparacion'

    ID_REPARACION = Column(Integer, primary_key=True)
    ID_TALLER = Column(ForeignKey('taller.ID_TALLER'), index=True)
    ID_DET_CONTROL = Column(ForeignKey('detalle_control_empresa.ID_DET_CONTROL'), index=True)
    DESCRIP_REPARACION = Column(String(200))
    FECHA_REPARACION = Column(Date)
    COSTO = Column(Numeric(10, 2))
    ESTADO_REP = Column(String(20))
    ESTADO_REP_TALLER = Column(String(20))

    detalle_control_empresa = relationship('DetalleControlEmpresa', primaryjoin='Reparacion.ID_DET_CONTROL == DetalleControlEmpresa.ID_DET_CONTROL', backref='reparacions')
    taller = relationship('Taller', primaryjoin='Reparacion.ID_TALLER == Taller.ID_TALLER', backref='reparacions')


class Resource(Base):
    __tablename__ = 'resources'

    resource_id = Column(Integer, primary_key=True)
    resource_name = Column(String(100), nullable=False)
    resource_type = Column(String(30), nullable=False)
    parent_id = Column(Integer, index=True)
    ordering = Column(Integer, nullable=False, server_default=FetchedValue())
    owner_user_id = Column(ForeignKey('users.id', ondelete='SET NULL', onupdate='CASCADE'), index=True)
    owner_group_id = Column(ForeignKey('groups.id', ondelete='SET NULL', onupdate='CASCADE'), index=True)

    owner_group = relationship('Group', primaryjoin='Resource.owner_group_id == Group.id', backref='resources')
    owner_user = relationship('User', primaryjoin='Resource.owner_user_id == User.id', backref='resources')


class Taller(Base):
    __tablename__ = 'taller'

    ID_TALLER = Column(Integer, primary_key=True)
    ID_TIPO_REPARACION = Column(ForeignKey('tipo_reparacion.ID_TIPO_REPARACION'), index=True)
    NOMBRE_TALLER = Column(String(50))
    DIRECCION_TALLER = Column(String(200))
    TELEFONO_TALLER = Column(String(10))

    tipo_reparacion = relationship('TipoReparacion', primaryjoin='Taller.ID_TIPO_REPARACION == TipoReparacion.ID_TIPO_REPARACION', backref='tallers')


class TipoCosto(Base):
    __tablename__ = 'tipo_costo'

    ID_TIPO_COSTO = Column(Integer, primary_key=True)
    TIPO_COSTO = Column(String(50))


class TipoRemolque(Base):
    __tablename__ = 'tipo_remolque'

    ID_TIPO_REMOLQUE = Column(Integer, primary_key=True)
    NOMBRE_TIPO = Column(String(50))
    CAPACIDAD = Column(String(20))


class TipoReparacion(Base):
    __tablename__ = 'tipo_reparacion'

    ID_TIPO_REPARACION = Column(Integer, primary_key=True)
    TIPO_REPARACION = Column(String(100))


class Ubicacion(Base):
    __tablename__ = 'ubicacion'

    ID_UBICACION = Column(Integer, primary_key=True)
    ID_NIVEL = Column(ForeignKey('nivel.ID_NIVEL'), index=True)
    CORRELATIVO = Column(String(5))
    DISPOONIBLE = Column(Integer)

    nivel = relationship('Nivel', primaryjoin='Ubicacion.ID_NIVEL == Nivel.ID_NIVEL', backref='ubicacions')


class UbicacionBodega(Base):
    __tablename__ = 'ubicacion_bodega'

    ID_UBICACION_BODEGA = Column(Integer, primary_key=True)
    ID_UBICACION = Column(ForeignKey('ubicacion.ID_UBICACION'), index=True)
    ID_VEHICULO = Column(ForeignKey('vehiculo.ID_VEHICULO'), index=True)
    OBSERVACION = Column(String(100))
    FECHAINGRESO = Column(Date)
    FECHAEGRESO = Column(Date)
    EGRESO = Column(Integer)

    ubicacion = relationship('Ubicacion', primaryjoin='UbicacionBodega.ID_UBICACION == Ubicacion.ID_UBICACION', backref='ubicacion_bodegas')
    vehiculo = relationship('Vehiculo', primaryjoin='UbicacionBodega.ID_VEHICULO == Vehiculo.ID_VEHICULO', backref='ubicacion_bodegas')


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    user_name = Column(String(128), unique=True)
    user_password = Column(String(256))
    email = Column(String(100), nullable=False, unique=True)
    status = Column(SmallInteger, nullable=False)
    security_code = Column(String(256))
    last_login_date = Column(DateTime)
    registered_date = Column(DateTime)
    security_code_date = Column(DateTime, server_default=FetchedValue())


class UsersGroup(Base):
    __tablename__ = 'users_groups'

    group_id = Column(ForeignKey('groups.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    user_id = Column(ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)
    create_date = Column(DateTime)

    group = relationship('Group', primaryjoin='UsersGroup.group_id == Group.id', backref='users_groups')
    user = relationship('User', primaryjoin='UsersGroup.user_id == User.id', backref='users_groups')


class UsersPermission(Base):
    __tablename__ = 'users_permissions'

    perm_name = Column(String(64), primary_key=True, nullable=False)
    user_id = Column(ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)

    user = relationship('User', primaryjoin='UsersPermission.user_id == User.id', backref='users_permissions')


class UsersResourcesPermission(Base):
    __tablename__ = 'users_resources_permissions'

    resource_id = Column(ForeignKey('resources.resource_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    perm_name = Column(String(64), primary_key=True, nullable=False)
    user_id = Column(ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)

    resource = relationship('Resource', primaryjoin='UsersResourcesPermission.resource_id == Resource.resource_id', backref='users_resources_permissions')
    user = relationship('User', primaryjoin='UsersResourcesPermission.user_id == User.id', backref='users_resources_permissions')


class Vehiculo(Base):
    __tablename__ = 'vehiculo'

    ID_VEHICULO = Column(Integer, primary_key=True)
    ID_ESTADO = Column(ForeignKey('estado_veh.ID_ESTADO'), index=True)
    ID_MODELO = Column(ForeignKey('modelo.ID_MODELO'), ForeignKey('modelo.ID_MODELO'), index=True)
    ID_IMPORTACION = Column(ForeignKey('importacion.ID_IMPORTACION'), index=True)
    LINEA_ESTILO = Column(String(40))
    CHASIS = Column(String(50))
    ANO = Column(Integer)
    NUM_MOTOR = Column(String(50))
    VIN = Column(String(50))
    COLOR = Column(String(20))
    CLASE = Column(String(20))
    TIPO_COMBUSTIBLE = Column(String(20))
    CAPACIDAD = Column(String(20))
    CILINDROS = Column(Integer)
    POLIZA = Column(String(10))
    PRECIO_VEHICULO = Column(Numeric(10, 2))
    FOTO_VEH = Column(LONGBLOB)
    PLACA = Column(String(10))

    importacion=relationship('Importacion', primaryjoin='Vehiculo.ID_IMPORTACION == Importacion.ID_IMPORTACION', backref='importaciones')
    estado_veh = relationship('EstadoVeh', primaryjoin='Vehiculo.ID_ESTADO == EstadoVeh.ID_ESTADO', backref='vehiculoes')
    modelo = relationship('Modelo', primaryjoin='Vehiculo.ID_MODELO == Modelo.ID_MODELO', backref='modelo_vehiculoes')
    modelo1 = relationship('Modelo', primaryjoin='Vehiculo.ID_MODELO == Modelo.ID_MODELO', backref='modelo_vehiculoes_0')


class Venta(Base):
    __tablename__ = 'venta'

    ID_VENTA = Column(Integer, primary_key=True)
    ID_CLIENTE = Column(ForeignKey('cliente.ID_CLIENTE'), index=True)
    ID_DET_CONTROL = Column(ForeignKey('detalle_control_empresa.ID_DET_CONTROL'), index=True)
    ID_EMPLEADO = Column(ForeignKey('empleado.ID_EMPLEADO'), index=True)
    DESCRIP_VENTA = Column(String(200))
    FECHA_VENTA = Column(Date)
    PRECIO_VENTA = Column(Numeric(10, 2))

    cliente = relationship('Cliente', primaryjoin='Venta.ID_CLIENTE == Cliente.ID_CLIENTE', backref='ventas')
    detalle_control_empresa = relationship('DetalleControlEmpresa', primaryjoin='Venta.ID_DET_CONTROL == DetalleControlEmpresa.ID_DET_CONTROL', backref='ventas')
    empleado = relationship('Empleado', primaryjoin='Venta.ID_EMPLEADO == Empleado.ID_EMPLEADO', backref='ventas')
