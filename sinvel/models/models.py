# coding: utf-8
from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, Numeric, SmallInteger, String, Text, Time
from sqlalchemy.orm import relationship
from sqlalchemy.schema import FetchedValue
from sqlalchemy.ext.declarative import declarative_base



Base = declarative_base()
metadata = Base.metadata


class AlembicZigguratFoundationsVersion(Base):
    __tablename__ = 'alembic_ziggurat_foundations_version'

    version_num = Column(String(32), primary_key=True)


class Empleado(Base):
    __tablename__ = 'empleado'

    ID_EMPLEADO = Column(Integer, primary_key=True)
    NOMBRE = Column(String(100), nullable=False)
    APELLIDO = Column(String(100), nullable=False)
    GENERO = Column(String(20), nullable=False)
    FECHA_NACIMIENTO = Column(Date, nullable=False)
    DUI = Column(String(9), nullable=False)
    NIT = Column(String(50), nullable=False)
    AFP = Column(String(50), nullable=False)
    ISSS = Column(String(50), nullable=False)
    ID_BODEGA = Column(ForeignKey('bodega.ID_BODEGA'), nullable=False, index=True)
    ID_USER = Column(ForeignKey('users.id', ondelete='SET NULL'), index=True)

    bodega = relationship('Bodega', primaryjoin='Empleado.ID_BODEGA == Bodega.ID_BODEGA', backref='empleadoes',lazy='subquery')
    user = relationship('User', primaryjoin='Empleado.ID_USER == User.id', backref='empleadoes',lazy='subquery')

class Bodega(Base):

    __tablename__ = 'bodega'

    ID_BODEGA = Column(Integer, primary_key=True)
    NOMBRE_BODEGA = Column(String(50))
    DESCRIPCION_BODEGA = Column(String(200))
    DIRECCION_BODEGA = Column(String(200))
    DEPARTAMENTO = Column(String(50))
    MUNICIPIO = Column(String(50))


class ControlEmpresa(Base):
    __tablename__ = 'control_empresa'

    ID_CONTROL = Column(Integer, primary_key=True)
    ID_VEHICULO = Column(ForeignKey('vehiculo.ID_VEHICULO'), index=True)
    ID_IMPORTADOR = Column(ForeignKey('importador.ID_IMPORTADOR'), index=True)
    TIPO_CONTROL = Column(String(20))
    DESCRIPCION_CONTROL = Column(String(200))
    HORA_CONTROL = Column(Time)
    FECHA_CONTROL = Column(Date)

    importador = relationship('Importador', primaryjoin='ControlEmpresa.ID_IMPORTADOR == Importador.ID_IMPORTADOR', backref='control_empresas')
    vehiculo = relationship('Vehiculo', primaryjoin='ControlEmpresa.ID_VEHICULO == Vehiculo.ID_VEHICULO', backref='control_empresas')


class Costo(Base):
    __tablename__ = 'costo'

    ID_COSTO = Column(Integer, primary_key=True)
    ID_TIPO_COSTO = Column(ForeignKey('tipo_costo.ID_TIPO_COSTO'), index=True)
    ID_VEHICULO = Column(ForeignKey('vehiculo.ID_VEHICULO'), index=True)
    DESCRIP_COSTO = Column(String(100))
    MONTO = Column(Numeric(10, 2))

    tipo_costo = relationship('TipoCosto', primaryjoin='Costo.ID_TIPO_COSTO == TipoCosto.ID_TIPO_COSTO', backref='costoes')
    vehiculo = relationship('Vehiculo', primaryjoin='Costo.ID_VEHICULO == Vehiculo.ID_VEHICULO', backref='costoes')


class DetalleImportacion(Base):
    __tablename__ = 'detalle_importacion'

    ID_DETALLE_IMPORT = Column(Integer, primary_key=True)
    ID_VEHICULO = Column(ForeignKey('vehiculo.ID_VEHICULO'), index=True)
    ID_IMPORTACION = Column(ForeignKey('importacion.ID_IMPORTACION'), index=True)
    DETALLE_DESPERFECTO = Column(String(400))

    importacion = relationship('Importacion', primaryjoin='DetalleImportacion.ID_IMPORTACION == Importacion.ID_IMPORTACION', backref='detalle_importacions')
    vehiculo = relationship('Vehiculo', primaryjoin='DetalleImportacion.ID_VEHICULO == Vehiculo.ID_VEHICULO', backref='detalle_importacions')


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
    ID_BODEGA = Column(ForeignKey('bodega.ID_BODEGA'), index=True)
    NUM_REGISTRO = Column(Integer)
    FECHA_IMP = Column(Date)
    PESO = Column(Numeric(10, 2))
    VALOR_ADUANERO = Column(Numeric(10, 2))
    CANTIDAD = Column(Integer)
    VALOR_FACTURADO = Column(Numeric(10, 2))
    PAIS_ORIGEN = Column(String(50))

    bodega = relationship('Bodega', primaryjoin='Importacion.ID_BODEGA == Bodega.ID_BODEGA', backref='importacions')
    importador = relationship('Importador', primaryjoin='Importacion.ID_IMPORTADOR == Importador.ID_IMPORTADOR', backref='importacions')


class Importador(Base):
    __tablename__ = 'importador'

    ID_IMPORTADOR = Column(Integer, primary_key=True)
    NOMBRE = Column(String(50))
    APELLIDO = Column(String(50))
    GENERO = Column(String(20))
    ID_USER = Column(ForeignKey('users.id', ondelete='SET NULL'), index=True)
    FECHA_NACIMIENTO = Column(Date)
    TELEFONO_CASA = Column(String(9))
    TELEFONO_CELULAR = Column(String(9))
    CORREO_IMPORTADOR = Column(String(60))
    RESPONSABLE = Column(String(100))
    NIT = Column(String(18))
    DUI = Column(String(10))
    APELLIDO_CASADA = Column(String(40))

    user = relationship('User', primaryjoin='Importador.ID_USER == User.id', backref='importadors')


class Inventario(Base):
    __tablename__ = 'inventario'

    ID_INVENTARIO = Column(Integer, primary_key=True)
    ID_VEHICULO = Column(ForeignKey('vehiculo.ID_VEHICULO'), index=True)
    CANT_DISPONIBLE = Column(Integer)
    CANT_MINIMA = Column(Integer)
    CANT_MAX = Column(Integer)

    vehiculo = relationship('Vehiculo', primaryjoin='Inventario.ID_VEHICULO == Vehiculo.ID_VEHICULO', backref='inventarios')


class Model(Base):
    __tablename__ = 'models'

    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)
    value = Column(Integer)


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
    ID_CONTROL = Column(ForeignKey('control_empresa.ID_CONTROL'), index=True)
    ID_TIPO_REMOLQUE = Column(ForeignKey('tipo_remolque.ID_TIPO_REMOLQUE'), index=True)
    ID_BODEGA = Column(ForeignKey('bodega.ID_BODEGA'), index=True)
    DESCRIP_REMOLQUE = Column(String(200))
    NOMBRE_REMOLQUE = Column(String(100))

    bodega = relationship('Bodega', primaryjoin='Remolque.ID_BODEGA == Bodega.ID_BODEGA', backref='remolques')
    control_empresa = relationship('ControlEmpresa', primaryjoin='Remolque.ID_CONTROL == ControlEmpresa.ID_CONTROL', backref='remolques')
    tipo_remolque = relationship('TipoRemolque', primaryjoin='Remolque.ID_TIPO_REMOLQUE == TipoRemolque.ID_TIPO_REMOLQUE', backref='remolques')


class Reparacion(Base):
    __tablename__ = 'reparacion'

    ID_REPARACION = Column(Integer, primary_key=True)
    ID_VEHICULO = Column(ForeignKey('vehiculo.ID_VEHICULO'), index=True)
    ID_TALLER = Column(ForeignKey('taller.ID_TALLER'), index=True)
    DESCRIP_REPARACION = Column(String(200))
    FECHA_REPARACION = Column(Date)

    taller = relationship('Taller', primaryjoin='Reparacion.ID_TALLER == Taller.ID_TALLER', backref='reparacions')
    vehiculo = relationship('Vehiculo', primaryjoin='Reparacion.ID_VEHICULO == Vehiculo.ID_VEHICULO', backref='reparacions')


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
    NOMBRE_TALLER = Column(String(50))
    DIRECCION_TALLER = Column(String(200))
    TELEFONO_TALLER = Column(String(10))


class TipoCosto(Base):
    __tablename__ = 'tipo_costo'

    ID_TIPO_COSTO = Column(Integer, primary_key=True)
    TIPO_COSTO = Column(String(50))


class TipoRemolque(Base):
    __tablename__ = 'tipo_remolque'

    ID_TIPO_REMOLQUE = Column(Integer, primary_key=True)
    NOMBRE_TIPO = Column(String(50))
    CAPACIDAD = Column(String(20))


class UbicacionBodega(Base):
    __tablename__ = 'ubicacion_bodega'

    ID_UBICACION = Column(Integer, primary_key=True)
    ID_NIVEL = Column(ForeignKey('nivel.ID_NIVEL'), index=True)
    ID_CONTROL = Column(ForeignKey('control_empresa.ID_CONTROL'), index=True)
    CORRELATIVO = Column(String(5))
    DISPOONIBLE = Column(Integer)

    control_empresa = relationship('ControlEmpresa', primaryjoin='UbicacionBodega.ID_CONTROL == ControlEmpresa.ID_CONTROL', backref='ubicacion_bodegas')
    nivel = relationship('Nivel', primaryjoin='UbicacionBodega.ID_NIVEL == Nivel.ID_NIVEL', backref='ubicacion_bodegas')


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
    LINEA_ESTILO = Column(String(40))
    MARCA = Column(String(30))
    MODELO = Column(String(30))
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
    FOTO_VEH = Column(String(200))

    estado_veh = relationship('EstadoVeh', primaryjoin='Vehiculo.ID_ESTADO == EstadoVeh.ID_ESTADO', backref='vehiculoes')


class Venta(Base):
    __tablename__ = 'venta'

    ID_VENTA = Column(Integer, primary_key=True)
    ID_VEHICULO = Column(ForeignKey('vehiculo.ID_VEHICULO'), index=True)
    DESCRIP_VENTA = Column(String(200))
    FECHA_VENTA = Column(Date)
    PRECIO_VENTA = Column(Numeric(10, 2))

    vehiculo = relationship('Vehiculo', primaryjoin='Venta.ID_VEHICULO == Vehiculo.ID_VEHICULO', backref='ventas')
