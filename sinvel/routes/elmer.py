def includeme(config):
    ##############EXAMPLES###############
    config.add_route('bodegas', '/bodegas')
    config.add_route('detalle_bodega', '/bodega/detalle/{id_bod}')
    config.add_route('registrarBodega', '/registro_bodega')
    config.add_route('registroBodegaGuardar', '/reg_bodega_guardar')
    config.add_route('ponerEnVenta', '/vehiculo/{id_veh}/vender')
    config.add_route('ventaVehiculoActualizar', '/venta_vehiculo_actualizar')
    config.add_route('asignarVendedor', '/vehiculo/{id_veh}/asignar')
    config.add_route('actualizarVendedor', '/actualizar_vendedor')
    config.add_route('detalleVehiculo', '/vehiculo/{id_veh}/{id_ven}/detalle')
    config.add_route('detalleVehiculoCliente', '/vehiculo/{id_veh}/{id_ven}/detalle_cliente')
    config.add_route('vehiculosAsignados', '/vehiculos_asignados')
    config.add_route('updateVenta', '/vehiculo/{id_veh}/{id_ven}/vender')
    config.add_route('actualizarVenta', '/actualizar_venta')
    #################################3###
    config.add_route('wizard', '/wizard')
    config.add_route('vehiculos', '/vehiculos')
