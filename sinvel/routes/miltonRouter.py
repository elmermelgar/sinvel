def includeme(config):
    ##############EXAMPLES###############
    config.add_route('list_importadores', '/importadores')
    config.add_route('vehiculo', '/vehiculos/subirFotos/{id_detImp}')
    config.add_route('subir', '/subirFotos')
    config.add_route('buscar', '/buscarVehiculo')
    config.add_route('combo', '/fltradoMarca/{idmarca}')
    config.add_route('aux', '/aux')
    config.add_route('resultado', '/resultadoVehiculo/{marca}/{modelo}/{estado}/{anio}')
    config.add_route('detalle', '/detalleVehiculo/{id_veh}')

    #############CRUD tipoReparacion######################
    config.add_route('tipoReparacion_list', '/tipoReparacion/list')
    config.add_route('tipoReparacion_create', '/tipoReparacion/create')
    config.add_route('tipoReparacion_update', '/tipoReparacion/update/{id_tipoRep}')
    config.add_route('tipoReparacion_save', '/tipoReparacion/save')
    config.add_route('tipoReparacion_del', '/tipoReparacion/del/{id_tipoRep}')

    #############CRUD Taller######################
    config.add_route('taller_list', '/taller/list')
    config.add_route('taller_create', '/taller/create')
    config.add_route('taller_update', '/taller/update/{id_taller}')
    config.add_route('taller_save', '/taller/save')
    config.add_route('taller_del', '/taller/del/{id_taller}')
