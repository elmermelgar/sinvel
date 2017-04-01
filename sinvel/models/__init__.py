from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import configure_mappers
import zope.sqlalchemy

# import or define all models here to ensure they are attached to the
# Base.metadata prior to any initialization routines
from .mymodel import MyModel  # flake8: noqa
from .models import Importador
from .models import ControlEmpresa
from .models import Bodega
from .models import Costo
from .models import DetalleImportacion
from .models import EstadoVeh
from .models import FotosDesperfecto
from .models import Importacion
from .models import Inventario
from .models import Nivel
from .models import Remolque
from .models import Reparacion
from .models import Taller
from .models import TipoCosto
from .models import TipoRemolque
from .models import UbicacionBodega
from .models import Vehiculo
from .models import Venta
from .models import Empleado
from .models import User,Group,GroupsPermission,UsersGroup,Resource,UsersPermission,UsersResourcesPermission
from .root_factory import RootFactory
from .resource_factory import ResourceFactory

# run configure_mappers after defining all of the models to ensure
# all relationships can be setup
configure_mappers()


def get_engine(settings, prefix='sqlalchemy.'):
    return engine_from_config(settings, prefix)

def get_session_callable(request):
    return request.dbsession

def get_session_factory(engine):
    factory = sessionmaker()
    factory.configure(bind=engine)
    return factory


def get_tm_session(session_factory, transaction_manager):
    """
    Get a ``sqlalchemy.orm.Session`` instance backed by a transaction.

    This function will hook the session to the transaction manager which
    will take care of committing any changes.

    - When using pyramid_tm it will automatically be committed or aborted
      depending on whether an exception is raised.

    - When using scripts you should wrap the session in a manager yourself.
      For example::

          import transaction

          engine = get_engine(settings)
          session_factory = get_session_factory(engine)
          with transaction.manager:
              dbsession = get_tm_session(session_factory, transaction.manager)

    """
    dbsession = session_factory()
    zope.sqlalchemy.register(
        dbsession, transaction_manager=transaction_manager)
    return dbsession


def includeme(config):
    """
    Initialize the model for a Pyramid app.

    Activate this setup using ``config.include('sinvel.models')``.

    """
    settings = config.get_settings()

    # use pyramid_tm to hook the transaction lifecycle to the request
    config.include('pyramid_tm')

    session_factory = get_session_factory(get_engine(settings))
    config.registry['dbsession_factory'] = session_factory

    # make request.dbsession available for use in Pyramid
    config.add_request_method(
        # r.tm is the transaction manager used by pyramid_tm
        lambda r: get_tm_session(session_factory, r.tm),
        'dbsession',
        reify=True
    )
