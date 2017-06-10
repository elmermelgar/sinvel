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
