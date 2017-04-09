
    $(function() {
     function verificar_correo (id) {
            $.getJSON("http://localhost:6543/AgregarImportador/VerificarUsuario/"+id, function(data){
            console.log(data);
            if (data.ID_IMPORTACION!==null)
                $('#idimportacion').html(data.ID_IMPORTACION);
                $('#importador').html(data.IMPORTADOR);
                $('#fecha_importacion').html(data.FECHA_IMPORTACION);
                $('#select').html('<input type="checkbox" id="cimportacion"/>');
                    // var target = $('#table');
                    // target.empty();
                    // $.each(data, function (key, val) {
                    //     target.append('<td>' + val + '</td>');
                    // });
                 $("#cimportacion").click( function(){
                    if( $(this).is(':checked') ){
                        $('#himportancion').val(data.ID_IMPORTACION);
                    }
                 });

        });
    }
    $('#verificar').click(function () {
        var CORREO_IMPORTADOR=null;

        id_importador=$('#id_importador ').val();
        if (id_importador!==null)
            verificar_correo(id_importador);
    });
});
