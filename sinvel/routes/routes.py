def includeme(config):
    #config.add_static_view('static', 'static', cache_max_age=3600)
    #config.add_route('home', '/{resource_id}')
    config.add_route('home', '/')


    config.add_route('prueba', '/prueba')
    config.add_route('inicio', '/inicio')
    config.add_route('registrar_vehiculo','/RegistrarVehiculo')
    config.add_route('buscar_importacion','/RegistrarVehiculo/BuscarImportacion/{id_importacion}')
    config.add_route('guardar_registro_vehiculo','/RegistrarVehiculo/guardar')
    config.add_route('models','/models/{id_marca}/all_json_models')
    #config.add_route('buscar_importacion', '/RegistrarVehiculo/BuscarImportacion?id_import={id_importacion}')
    #config.add_route('registrar_vehiculo', '/RegistroVehiculo/{id_importacion}')

    ##prueba para envio##


    ############Seguridad################
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('user_register', '/user/register')
    config.add_route('user_create', '/user/create')
    ######################################

    config.add_route('generar_reporte', '/generar')


    ############IMPORTADOR Y COSTOS###################
    config.add_route('agregar_importador', '/AgregarImportador')
    config.add_route('costo_veh', '/costo_vehiculo/{id_vehiculo}')
    config.add_route('detalle_costo', '/detalle_costo/{id_costo}')
    config.add_route('guardar_importador', '/AgregarImportador/guardar')
    config.add_route('agregar_remolque', '/AgregarRemolque')
    config.add_route('guardar_remolque', '/AgregarRemolque/guardar')
    config.add_route('remolque_list', '/remolque/list')
    config.add_route('delete_remolque', '/remolque/delete/{id_remolque}')
    config.add_route('importador_delete', '/importador/delete/{id_importador}')
    config.add_route('importador_list', '/importador/list')



    #################Salida Reparacion#############
    config.add_route('verificar_remolque', '/salida_reparacion/verificar_remolque')
    config.add_route('registro_control', '/salida_reparacion/registro_control')
    config.add_route('registro_control_guardar', '/salida_reparacion/registro_control/save')
    config.add_route('registro_control_venta', '/salida_venta/registro_control/save')
    config.add_route('aprobar_salidas', '/salida_reparacion/aprobar_salidas')
    config.add_route('aprobar_salidas_guardar', '/salida_reparacion/aprobar_salidas/save')
    config.add_route('buscar_tipo_remolque', '/salida_reparacion/verificar_remolque/{id_tipo_remolque}')

    #################Salida Reparacion#############
    config.add_route('salidaVenta', '/salida_venta/aprobar')

    ################Entradas#######################
    config.add_route('registro_control_entrada','/entrada/registro_control_entrada')
    config.add_route('registro_entrada_control_guardar','/entrada/registro_entrada_control_guardar')
    config.add_route('registro_control_entrada_reparacion','/entrada/registro_control_entrada_reparacion')
    config.add_route('registro_control_entrada_reparacion_guardar','/entrada/registro_control_entrada_reparacion_guardar')


    ###############Alertas por multas##############
    config.add_route('alerta_multa','/alerta_multa')
    config.add_route('alerta_multa_cantidad_vehiculos','/alerta_multa/cantidad')


    #############CRUD Empleado######################


    config.add_route('empleado_list','/empleado/list')
    config.add_route('empleado_create','/empleado/create')
    config.add_route('guardar_empleado','/empleado/save')
    config.add_route('empleado_edit','/empleado/edit/{id_empleado}')
    config.add_route('empleado_delete','/empleado/delete/{id_empleado}')

    config.add_route('remolques', '/get_remolques')
    config.add_route('gestion_remolque', '/remolques/gestion_remolques')
    config.add_route('vehiculos_buscar_bodeguero', '/bodega/vehiculos')