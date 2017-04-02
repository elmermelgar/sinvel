/**
 * Created by David-PC on 2/4/2017.
 */

    $(function() {
     function buscar_importacion (id) {
            $.getJSON("http://localhost:6543/RegistrarVehiculo/BuscarImportacion/"+id, function(data){
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
    $('#buscar').click(function () {
        var id_importacion=null;
        id_importacion=$('#id_importacion ').val();
        if (id_importacion!==null)
            buscar_importacion(id_importacion);
    });
});
