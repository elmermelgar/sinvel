def includeme(config):
    ##############EXAMPLES###############
    config.add_route('list_importadores', '/importadores')
    config.add_route('list_vehiculos', '/vehiculos/{id_imp}')
    config.add_route('vehiculo', '/vehiculos/subirFotos/{id_imp}/{id_veh}')
    config.add_route('subir', '/subirFotos')