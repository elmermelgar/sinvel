def includeme(config):
    ##############EXAMPLES###############
    config.add_route('bodegas', '/bodegas')
    config.add_route('detalle_bodega', '/bodega/detalle/{id_bod}')
    config.add_route('registrarBodega', '/registro_bodega')
    config.add_route('registroBodegaGuardar', '/reg_bodega_guardar')
    config.add_route('ponerEnVenta', '/vehiculo/{id_veh}/vender')
    config.add_route('ventaVehiculoActualizar', '/venta_vehiculo_actualizar')

    #################################3###
    config.add_route('wizard', '/wizard')
    config.add_route('vehiculos', '/vehiculos')
