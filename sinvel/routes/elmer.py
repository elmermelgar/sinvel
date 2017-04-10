def includeme(config):
    ##############EXAMPLES###############
    config.add_route('bodegas', '/bodegas')
    config.add_route('detalle_bodega', '/bodega/detalle/{id_bod}')



    #################################3###
    config.add_route('wizard', '/wizard')
