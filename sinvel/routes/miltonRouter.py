def includeme(config):
    ##############EXAMPLES###############
    config.add_route('list_importadores', '/importadores')
    config.add_route('list_vehiculos', '/vehiculos/{id_detImp}')
    config.add_route('vehiculo', '/vehiculo/subirFotos/{id_imp}/{id_veh}')
    config.add_route('subir', '/subirFotos')