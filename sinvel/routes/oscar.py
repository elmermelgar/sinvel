def includeme(config):
    config.add_route('registroImportacion', '/registro_importacion')
    config.add_route('registroImportacionGuardar', '/reg_import_guardar')
    config.add_route('ubiVehSeleccionar', '/uv_sel_ubicacion/{idv}')
    config.add_route('ubiVehGuardar', '/uv_guardar_ubicacion/{idv}/{idu}')
    config.add_route('enviarVehReparar', '/enviar_veh_reparar/{idv}')
    config.add_route('filterTalleres', '/tipoRep/{idtrep}/busqtalleres')
    config.add_route('enviarVehRepararGuardar','/enviar_veh_reparar_save')