def includeme(config):
    ##############EXAMPLES###############
    config.add_route('list_importadores', '/importadores')
    config.add_route('list_vehiculos', '/vehiculos/{id_imp}')
    config.add_route('vehiculo', '/vehiculos/subirFotos/{id_imp}/{id_detImp}/{id_veh}')
    config.add_route('subir', '/subirFotos')
    config.add_route('buscar', '/buscarVehiculo')
    config.add_route('combo', '/fltradoMarca/{idmarca}')
    config.add_route('resultado', '/resultadoVehiculo')
    config.add_route('detalle', '/detalleVehiculo/{id_veh}')
