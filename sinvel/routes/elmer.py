def includeme(config):
    ##############EXAMPLES###############
    config.add_route('bodegas', '/bodegas')
    config.add_route('detalle_bodega', '/bodega/detalle/{id_bod}')
    config.add_route('registrarBodega', '/registro_bodega')
    config.add_route('registroBodegaGuardar', '/reg_bodega_guardar')

    #################################3###
    config.add_route('wizard', '/wizard')
