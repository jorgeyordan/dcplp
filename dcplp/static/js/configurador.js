
//LO PRIMERO OBTENER EL LISTADO DE TERMINALES iew


// ******************AÑADIR Y ELIMINAR FILAS***************************************************
$(document).on('click', '#dale', function(){

  //obtener cuántas filas hay
  var n = $("#principal").children().length;

  //si es menor que 9 filas...
  if (n<9){
    var nuevo_elemento = $("#grupo").clone();
    nuevo_elemento.attr("id", "grupo" + n);
    nuevo_elemento.appendTo($("#principal"));

    $("#grupo" + n + " " + "#id_n_altas").attr("id", "id_n_altas" + n);
    $("#grupo" + n + " " + "#id_tarifa").attr("id", "id_tarifa" + n);
    $("#grupo" + n + " " + "#id_origen").attr("id", "id_origen" + n);
    $("#grupo" + n + " " + "#id_voz_datos").attr("id", "id_voz_datos" + n);
    $("#grupo" + n + " " + "#id_cv").attr("id", "id_cv" + n);
    $("#grupo" + n + " " + "#id_mfo").attr("id", "id_mfo" + n);
    $("#grupo" + n + " " + "#id_vap").attr("id", "id_vap" + n);
    $("#grupo" + n + " " + "#id_terminales").attr("id", "id_terminales" + n);
    $("#grupo" + n + " " + "#id_terminales_iew").attr("id", "id_terminales_iew" + n);

// POR DEFECTO AL GENERAR NUEVA FILA MOSTRAR LOS TERMINALES DE MULTILINEA Y HABILITAR TODOS LOS CAMPOS
$("#id_terminales_iew"+n).css('display', 'none');
$("#id_terminales"+n).css('display', 'block');

$("#id_voz_datos"+n).prop("disabled",false);
$("#id_cv"+n).prop("disabled",false);
$("#id_mfo"+n).prop("disabled",false);

//incluir el número de fila en el circulo
nuevo_elemento.find('h5').text(n+1);


} //fin si n<9



else{
  swal("En serio?!", "...Lo siento, solo estoy preparado para 9 configuraciones diferentes!");
}
});

//ELIMINAR FILAS ( BOTON ELIMINAR)
$('#elimina').click(function(){
// eliminar las filas de configuración
var n = $("#principal").children().length;
 if (n>=2){
$('#grupo' + (n-1)).hide('slow').remove();
}

//ELIMINAR CUADROS resumen ( BOTON ELIMINAR)
//get number of visible divs which contains tarjeta in id
  var j = $("div[id*='tarjeta']:visible").length;


//hide last visible div
$('#tarjeta' + (j-3)).hide("slow");

//remove image appended
$('#imagen_div' + (j-3)).hide("slow");

//si solo hay uno, eliminar tambien la de resumen
if(j==3){
  $('#tarjeta_resumen').hide("slow");
};
//si ya está la tarjeta resumen mostrada, RECALCULAR
if ($("#tarjeta_resumen").is(':visible')){
$('#boton_buscar').trigger('click');
}

});


// ******************FUNCIÓN BOTON GENERAR!!!!**************************************************
// -------------------------------------------------------------------------------------------------

$(document).on('click', "#boton_buscar", function(event){



  //obtener el tipo de conecta SELECCIONADO
  var conecta_elegido = $("#id_conectas option:selected" ).text();

  //obtener cuántas filas hay
  n = $("#principal").children().length;
  event.preventDefault();

  //Obtener todos los campos del formulario visibles rellenados
  //---------------------------------------------------
  //es decir, cuantas líneas, por cada tipo de qué tarifa, etc etc
  var n = $("#principal").children().length;
    lineas =[];
    var miarray = [];
    for (var i = 1; i<=n; i++) {
      if (i==1){

        //antes de hacer el array de datos obtenidos, necesito saber si es multilinea o no
        var tarifa_seleccionada = $("#id_tarifa").val();
        if (tarifa_seleccionada!='optima' && tarifa_seleccionada!='optima_rpv' && tarifa_seleccionada!='solper'){//SELECCIONO IEW PRO
          var terminal_array = $("#id_terminales_iew").val()}
        else{var terminal_array =$("#id_terminales").val()}


        //meter todos los datos en array
        var miarray = [
          $("#id_n_altas").val(),
          $("#id_tarifa").val(),
          $("#id_origen").val(),
          $("#id_voz_datos").val(),
          $("#id_cv").val(),
          $("#id_mfo").val(),
          $("#id_vap").val(),
          terminal_array,
          ];
      lineas.push(miarray);
    } //fin bloque if (si es el primer elemento)

      else {
        //antes de hacer el array de datos obtenidos, necesito saber si es multilinea o no
        var tarifa_seleccionada = $("#id_tarifa"+ (i-1)).val();
        if (tarifa_seleccionada!='optima' && tarifa_seleccionada!='optima_rpv' && tarifa_seleccionada!='solper'){//SELECCIONO IEW PRO
          var terminal_array = $("#id_terminales_iew"+ (i-1)).val()}
        else{var terminal_array =$("#id_terminales"+ (i-1)).val()}

        //meter los datos en array
        var miarray = [
        $("#id_n_altas" + (i-1)).val(),
        $("#id_tarifa" + (i-1)).val(),
        $("#id_origen" + (i-1)).val(),
        $("#id_voz_datos" + (i-1)).val(),
        $("#id_cv" + (i-1)).val(),
        $("#id_mfo" + (i-1)).val(),
        $("#id_vap" + (i-1)).val(),
        terminal_array,
        ];
        lineas.push(miarray);
      } //fin bloque else
    } //fin for

    //crear variable para obtener datos de cpc
    var conecta_elegido = $("#id_conectas option:selected" ).text();

    //si el conecta elegido es un cpc......
    if (conecta_elegido.substring(0,3)=='CPC'){
      if (sessionStorage.getItem('datos_cpc')){
        var datos_cpc = sessionStorage.getItem('datos_cpc');
      }
} //fin, si conecta elegido es cpc
  else{
    var datos_cpc = 'sin_cpc'
  }



    //---------------------------------------------------

  $.ajax({
    url: 'configurador_ajax',
    data: {
      'datos':lineas,
      'conecta':conecta_elegido,
      'cpc':datos_cpc
    },
    dataType: 'json',


     // handle a successful response
    success: function(data) {
      datostraidosdedjando = data;
      if (data) {

        total_lineas =0;
        var total_rentabilidad = 0;
        var total_comisiones = 0;

      //mostrar la tarjeta RESUMEN
      mostrarDIV('tarjeta_resumen');

      //recorrer todos los array obtenido para crear los resultados
      for(var i = 0;i<data.length;i++){

        //inicializo ya algunas variables:
        var modelo = data[i]['modelo'];
        var unidades = data[i]['unidades'];
        var rent =  data[i]['rent'];
        var total =  data[i]['total'];
        var aviso = data[i]['aviso'];
        var mgequipo = data[i]['dxc'] - data[i]['precio']

        //COLORES!!!!!
        //para cada una de las tarjetas: dependiendo si el total es bueno, el color de la fuente de un color u otro
        if (total>70){var color = 'green';}
        else if (total<0) {var color ='red';}
        else {var color ='blue';}


        //RECOMENDACIONES!
        mostrarDIV('tarjeta'+i);
        var recos = data[i]['todosaqui'];
        var gama_jorge = data[i]['gama_jorge'];

        if (recos !='Lo sentimos. No encontramos recomendaciones!' &&  data[i]['terminal_vap_reco_sobre_cliente']==true){
          var mensaje = 'El terminal elegido tiene margen cero y no podemos recomendarte nada que mejore la rentabiliad, pero los siguientes mejoran el pago total del cliente:</hr>';
        }

        else if (recos !='Lo sentimos. No encontramos recomendaciones!'){
          var mensaje = 'Has elegido un ' + gama_jorge + ' con un margen de equipo de: ' + mgequipo + '€. Los siguientes tienen un coste similar con una mejor rentabilidad:'
        }
        else{
          mensaje ='No hemos encontrado ningún equipo tipo ' + gama_jorge + ' de caracterísiticas similares que mejore la rentabilidad. Sorry!';
        }
        if (modelo=='sin_terminal'){var mensaje = 'Si quieres te recomiendo un tarjeta sim más barata?'}
        $( "#dialog" + i + " p").html(mensaje + '<ol>'+recos + '</ol>');


        //escribir encabezado y comisiones en tarjeta
        $("#encabezadoh"+i).html(modelo + " (" + rent + " €/línea)");
        var resultado = "<p> Comision datos: " + data[i]['datos'] + "</p>" +
          "<p> Comision voz: " + data[i]['voz'] + "</p>" +
          "<p> Comision Terminal: " + data[i]['extra'] + "</p>" +
          "<p> Subvención: " + data[i]['dxc'] + "</p>" +
          "<p> Precio Cesión: " + data[i]['precio'] + "</p>" +
          "<p> Comision Sva: " + data[i]['sva'] + "</p>" +
          "<p> Pago Cliente: " + data[i]['pvp'] + "</p>" +
          "<p> Cuota mes: " + data[i]['cuota'] + "</p>" +
          "<p><b><font color="+color+"> Comision Total: " + total + "</font></b></p>";
        $("#comisiones"+i).html(resultado);

        //escribir los avisos en tarjeta
        if(aviso){
          $("#avisos"+i).html("Avisos");
          $("#pavisos"+i).html(aviso);
          $('#tarjeta'+i+" .micard").css('border-color', 'red'); //si hay avisos poner el borde rojo


          }
        else{
          //si no hay avisos no escribir nada en ese párrafo
          $("#avisos"+i).html("");
          $("#pavisos"+i).html("");
          $('#tarjeta'+i+" .micard").css('border-color', 'grey'); //si ya estuviera puesto en rojo hay que ponerlo en gris
            }

        //incluir la imagen**************************************
        var nhijos = $("#imagen_div"+i).children().length;
        var srcimg = $("#imagen_div"+i).find('img').attr("src");


      if (srcimg!=data[i]['foto']){
          //eliminar la imagen que habíaf
          $("#imagen_div"+i).find('img[src$="'+srcimg+'"]').remove();

          //incluir la imagen nueva que había
          $("#imagen_div"+i).prepend(`<img src="/static/images/terminales_modelos/`+ data[i]['foto'] + `" height="142" width="142">`)

          //mostrarla (hago esto, porque pasaba que después de eliminar y volver a mostrar quedaba como display=none)
          $('#imagen_div' + i).css("display", "block");

        }


      else{
        $("#imagen_div"+i).show("slow");
      }

      //pasar a una variable el valor de gastos y pagos de cliente almacenado en sessionStorage
      if (sessionStorage.getItem('importe_ingreso_gasto')){
        var importe_ingreso_gasto = parseInt(sessionStorage.getItem('importe_ingreso_gasto'));
        var es_numero = typeof importe_ingreso_gasto === 'number' && isFinite(importe_ingreso_gasto); //check if is number

      }
      else{
        var importe_ingreso_gasto = 0;
      }
      if (es_numero=='false'){

        var importe_ingreso_gasto = 0;
      }





      //OBTENER EL SUMATORIO DE todas y calculos de totales
      total_comisiones = total_comisiones + (data[i]['voz'] + data[i]['extra'] + data[i]['sva'] + data[i]['datos'])*Number(unidades)
      comision_conecta = data[i]['comision_conecta']
      total_rentabilidad = total_rentabilidad+total+ importe_ingreso_gasto;
      total_lineas = total_lineas + Number(unidades);
      var rentabilidad_porLinea = (total_rentabilidad/total_lineas).toFixed(2);
      var total_rentabilidad_conFija = total_rentabilidad + comision_conecta;
      var comision_base_operaciones = data[i]['comision_base_operaciones'];
      var comision_acelerador_convergencia = data[i]['comision_conecta_operaciones'];
      var comision_acelerador_iew = data[i]['comision_iew_operaciones'];
      var volumen_movil =  data[i]['prima_volumen_movil'];
      var volumen_fijo =  data[i]['prima_volumen_fijo'];


    var total_rentabilidad_conApoyos =  (Number(total_rentabilidad_conFija) + Number(comision_base_operaciones) + Number(comision_acelerador_iew) + Number(volumen_movil) + Number(volumen_fijo)).toFixed(2);

    //COLORES PARA LA TARJETA RESUMEN!!!!!
    //rentabilidad por línea
    if (rentabilidad_porLinea>70){var color_por_linea = 'green';}
    else if (rentabilidad_porLinea<0) {var color_por_linea ='red';}
    else {var color_por_linea ='orange';}
    //upfrontfijo
    if (comision_conecta>0){var color_fijo = 'green';}
    else if (comision_conecta==0) {var color_fijo ='red';}






        //para coeficiente de Rentabilidad
        switch (true) {
          case (rentabilidad_porLinea < 30):
              coeficiente = 0;
              break;
          case (rentabilidad_porLinea < 50):
              coeficiente = 0.5;
              break;
          case (rentabilidad_porLinea < 70):
              coeficiente = 0.75;
              break;
          case (rentabilidad_porLinea < 80):
              coeficiente = 1;
              break;
          case (rentabilidad_porLinea >= 80):
              coeficiente = 1.25;
              break;
          default:
              coeficiente = 1;
              break;
      }


      //ESTO ES TODO LO QUE VOY  A MOSTRAR EN LA tabla
      var grupo_usuario =  data[i]['grupo_usuario'];
      if (grupo_usuario !='comercial'){
      var contenido_total = ('<table class="table table-striped table-sm table-dark">'+
      '<thead class="thead-light"><tr><th scope="col">concepto</th>' +
      '<th scope="col">importe</th></tr></thead><tbody>'+
    '<tr><td data-toggle="tooltip" data-placement="top" title="Esto es lo que genera la operación"><font color="yellow"><b>Rentabilidad Movil</b></font></td><td>'+ total_rentabilidad + '€</td></tr>' +
    '<tr><td data-toggle="tooltip" data-placement="top" title="Nº total de líneas configuradas. Determina algunas comisiones">Lineas:</td><td>'+ total_lineas + '</td></tr>' +
    '<tr><td data-toggle="tooltip" data-placement="top" title="Rentabilidad total de la operación entre líneas configuradas">Rentabilidad por línea:</td><td><font color="'+ color_por_linea + '">'+ rentabilidad_porLinea + '€</td></tr>' +
    '<tr><td data-toggle="tooltip" data-placement="top" title="Ingeso o gasto adicional de la operacion definido por el usuario">Otros pagos o ingresos:</td><td>'+ importe_ingreso_gasto + '€</td></tr>' +
    // '<tr><td data-toggle="tooltip" data-placement="top" title="Comisiones sin contar Dxc ni precio cesión">Total Comisiones:</td><td>'+ total_comisiones + '€</tr>' +
    // '<tr><td data-toggle="tooltip" data-placement="top" title="Para los asesores el modulador de rentabilidad en porcentaje">Coeficiente:</td><td>'+ coeficiente*100 + '%</tr>' +
    '<tr><td data-toggle="tooltip" data-placement="top" title="Comisión por el conecta Pymes">Upfront Fija:</td><td><font color="'+ color_fijo + '">'+ comision_conecta+ '€</font></td></tr>' +
    '<tr><td data-toggle="tooltip" data-placement="top" title="Esto es lo que genera la operación incluyendo la fija"><font color="yellow"><b>Rentabilidad Total</b></font></td><td>'+ total_rentabilidad_conFija + '€</td></tr>' +
    // '<tr><td data-toggle="tooltip" data-placement="top" title="Es un Cliente Valor?(Volumen)">Cliente Valor:</td><td>'+ cliente_valor+ '</tr>' +
    '<tr><td data-toggle="tooltip" data-placement="top" title="Prima de Volumen Móvil. tramo 70%(tramo3)">Volumen Móvil:</td><td>'+ volumen_movil+ '€</td></tr>' +
    '<tr><td data-toggle="tooltip" data-placement="top" title="Prima de Volumen Fijo. tramo 70/2%(tramo3)">Volumen Fijo:</td><td>'+ volumen_fijo+ '€</td></tr>' +
    '<tr><td data-toggle="tooltip" data-placement="top" title="Base multilínea de la prima de operaciones">Operaciones Base</td><td>'+ comision_base_operaciones+ '€</td></tr>' +
    '<tr><td data-toggle="tooltip" data-placement="top" title="Acelerador de convergencia en Prima de Operaciones">Acelerador Conecta</td><td>'+ comision_acelerador_convergencia+ '€</td></tr>' +
    '<tr><td data-toggle="tooltip" data-placement="top" title="Acelerador de IEW PRO en Prima de Operaciones">Acelerador IEW</td><td>'+ comision_acelerador_iew+ '€</td></tr>' +
    '<tr><td data-toggle="tooltip" data-placement="top" title="Esto es lo que genera la operación incluyendo fija y apoyos"><font color="yellow"><b>Rentabilidad Total</b></font></td><td>'+ total_rentabilidad_conApoyos + '€</td></tr>'+
  '</tbody></table>')
  }
  else{
    var contenido_total = ('<table class="table table-striped table-sm table-dark">'+
    '<thead class="thead-light"><tr><th scope="col">concepto</th>' +
    '<th scope="col">importe</th></tr></thead><tbody>'+
  '<tr><td data-toggle="tooltip" data-placement="top" title="Esto es lo que genera la operación"><font color="yellow"><b>Rentabilidad Movil</b></font></td><td>'+ total_rentabilidad + '€</td></tr>' +
  '<tr><td data-toggle="tooltip" data-placement="top" title="Nº total de líneas configuradas. Determina algunas comisiones">Lineas:</td><td>'+ total_lineas + '</td></tr>' +
  '<tr><td data-toggle="tooltip" data-placement="top" title="Rentabilidad total de la operación entre líneas configuradas">Rentabilidad por línea:</td><td><font color="'+ color_por_linea + '">'+ rentabilidad_porLinea + '€</td></tr>' +
  '<tr><td data-toggle="tooltip" data-placement="top" title="Ingeso o gasto adicional de la operacion definido por el usuario">Otros pagos o ingresos:</td><td>'+ importe_ingreso_gasto + '€</td></tr>' +
  // '<tr><td data-toggle="tooltip" data-placement="top" title="Comisiones sin contar Dxc ni precio cesión">Total Comisiones:</td><td>'+ total_comisiones + '€</tr>' +
  // '<tr><td data-toggle="tooltip" data-placement="top" title="Para los asesores el modulador de rentabilidad en porcentaje">Coeficiente:</td><td>'+ coeficiente*100 + '%</tr>' +
  '<tr><td data-toggle="tooltip" data-placement="top" title="Comisión por el conecta Pymes">Upfront Fija:</td><td><font color="'+ color_fijo + '">'+ comision_conecta+ '€</font></td></tr>' +
  '<tr><td data-toggle="tooltip" data-placement="top" title="Esto es lo que genera la operación incluyendo la fija"><font color="yellow"><b>Rentabilidad Total</b></font></td><td>'+ total_rentabilidad_conFija + '€</td></tr>' +
  '</tbody></table>')

  }



    $("#contenido_resumen").html(contenido_total);

color_por_linea


      }; //FINBUCLE FOR



        //escribir los avisos
        var aviso = data['aviso'];
        if(aviso){
        $("#avisos").html("Avisos");
        $("#pavisos").html(aviso);}
        else{
          $("#avisos").html("");
          $("#pavisos").html("");
        };


      } //fin if

    } //fi función success

  }); //fin ajax

});//fin de la función del boton generar/buscar al click


function mostrarDIV(nombre_div) {
var x = document.getElementById(nombre_div);
if (x.style.display === "none") {
  x.style.display = "inline-flex";
} else {
x.style.display = "inline-flex";
};
};



// POP UP*******************************

$(function() {
    $( "div[id*='dialog']" ).dialog({
      autoOpen: false,
      show: {
        effect: "blind",
        duration: 1000
      },
      hide: {
        effect: "explode",
        duration: 1000
      }
    });
  });//fin function


$(".btnpequejorge").click(function(e){
  var idClicked = e.target.id.slice(-1);
// swal("Here's the title!", "...and here's the text!");
$( "#dialog" + idClicked ).dialog( "open" );
});
// FIN POP UP*******************************

 //-------------------------------------------
 //SWEET ALERTS!!!!!!!
 //-------------------------------------------

 //boton de instrucciones
 // -----------------------
$('#boton_instrucciones').click(function(){
  swal.mixin({
  input: 'text',
  confirmButtonText: 'Next &rarr;',
  showCancelButton: true,
  progressSteps: ['1', '2', '3']
}).queue([
  {
    title: 'Question 1',
    text: 'Chaining swal2 modals is easy'
  },
  'Question 2',
  'Question 3'
]).then((result) => {
  if (result.value) {
    swal({
      title: 'All done!',
      html:
        'Your answers: <pre>' +
          JSON.stringify(result.value) +
        '</pre>',
      confirmButtonText: 'Lovely!'
    })
  } //fin : si el resultado existe....
  else{
    console.log('no has rellenado nada macho!');
    swal({
  position: 'top-end',
  type: 'success',
  title: 'Your work has been saved',
  showConfirmButton: false,
  timer: 1500
}) // fin swal en else
} //fin else (si no ha rellenado todo)
})
}); //fin click function







//BOTON DE INGRESOS Y gastos
// ******************************
$('#boton_otros').click(function(){


  swal({
    title:'Añadir importe',
    text:'Incluye el importe a añadir a la rentabilidad. En caso de gastos debe ser con signo negativo',
    input:'number',
    showCancelButton: true,
    confirmButtonText: 'Añadir',

})
.then(response => {

  // if ($('#tarjeta_resumen').is(":visible")){}

var respuesta = parseInt(response['value']);
  //comprobar que no está vacío
  if (response['value']=="") {
    swal({
      type: 'error',
      title: 'Oops...',
      text: 'Suponía que ibas a rellenar algo...',

    })
  }
  //comprobar que no cancela
  if (response['dismiss']=='cancel'){
    swal({
      type: 'error',
      title: 'Oops...',
      text: 'Has cancelado. Te has arrepentido?',

    })
    }

    //comprobar que es un número
    if (isNaN(respuesta)){ //si se introdujo texto, al hacer el parseint la variable se convirte en Not a Number
      swal({
        type: 'error',
        title: 'Oops...',
        text: 'No entiendo lo que dices, esperaba un número!',

      })
      }


  //si no esta vacio ni ha cancelado, si no es texto....
  else{
    sessionStorage.setItem('importe_ingreso_gasto', response['value']); //almacenar el importe del boton para pagos de clientes y otros gastos
    swal({
  position: 'top-end',
  type: 'success',
  title: 'Se han incluido ' + response['value'] + ' a la rentabilidad',
  showConfirmButton: false,
  timer: 1500
})
if ($("#tarjeta_resumen").is(':visible')){
$('#boton_buscar').trigger('click');
}

  } //fin else

});
});




//-------------------------------------------
//IEW PRO - QUE PASA SI SELECCIONO IEW PRO
//-------------------------------------------
// SI SELECCIONO IEW PRO, CAPAR DATOS Y MODIFICAR TERMINALES

$("body").on('change', "select[id*='id_tarifa']", function(e){
var idClicked2 = e.target.id.slice(-1);
//PRIMERO QUIERO OBTENER EL ID DEL ELEMENTO QUE ESTOY SELECCIONANDO
//si es el primer elemento, (fila1) idclicked no tiene número y sera ='a' por id_tarif_a
if (idClicked2=='a'){
  var select_datos = $("#id_voz_datos");
  var tarifa_seleccionada = $("#id_tarifa").val();
  var select_cv = $("#id_cv");
  var select_mfo = $("#id_mfo");
  var select_terminales = $("#id_terminales");
    var select_terminales_iew = $("#id_terminales_iew");
}
else{
  var select_datos = $("#id_voz_datos"+idClicked2);
  var tarifa_seleccionada = $("#id_tarifa"+idClicked2).val();
  var select_cv = $("#id_cv"+idClicked2);
  var select_mfo = $("#id_mfo"+idClicked2);
  var select_terminales = $("#id_terminales"+idClicked2);
  var select_terminales_iew = $("#id_terminales_iew"+idClicked2);
}
//DESPUÉS QUIERO VER SI LO QUE HE SELECCIONADO ES UN PINCHO
if (tarifa_seleccionada!='optima' && tarifa_seleccionada!='optima_rpv' && tarifa_seleccionada!='solper') //SELECCIONO IEW PRO
{
  //ahora cambiar el paquete de voz y datos a "sin datos" y luego disabled (asi como cv, y mfo)
  select_datos.val('sin_datos');
  select_cv.val('sin_cv');
  select_mfo.val('sin_mfo');

  select_datos.prop("disabled",true);
  select_cv.prop("disabled",true);
  select_mfo.prop("disabled",true);

  //cambiar los terminales (primero iba a reemplazar todos los options, pero creo que mejor, mostrar los dos y jugar con display)
//es decir, dependiendo de la tarifa mostrar select terminales multilínea o terminales iew
select_terminales.css("display", "none");
select_terminales_iew.css("display", "block");


}
else{//SI ES MULTILÍNA.....
  select_datos.prop("disabled",false);
  select_cv.prop("disabled",false);
  select_mfo.prop("disabled",false);
  //mostrar los terminales de multi y escondier los de iew
  select_terminales.css("display", "block");
  select_terminales_iew.css("display", "none");
} //fin si es multilínea

//además de todo esto, si la tarjeta resumen ya está visible, generar los resultaods
  if ($("#tarjeta_resumen").is(':visible')){
  $('#boton_buscar').trigger('click');
  }



});


//-------------------------------------------
//AL MODIFICAR EL SELECT DE CONECTA PYME
//-------------------------------------------
$('#id_conectas').change(function(){
  var conecta_elegido = $("#id_conectas option:selected" ).text();

  //si el conecta elegido es un cpc......
  if (conecta_elegido.substring(0,3)=='CPC'){
    sessionStorage.removeItem('datos_cpc');


    swal.mixin({
  input: 'number',
  confirmButtonText: 'Next &rarr;',
  showCancelButton: true,
  progressSteps: ['1', '2', '3']
}).queue([
  {
    title: 'PUESTOS COMUNICATOR?',
    text: 'Por favor, indica cuántos puestos comunicator tiene el CPC'
  },
  'PUESTOS FIJOS SIMPLES',
  'PESTOS FIJOS AVANZADOS'
]).then((result) => {

  //comprobar que no hay ningún valor vacio
if (result.value){
  var todoscpcrellenados = 0
  for(var i =0; i< result.value.length; i++){
    if (result.value[i]!=""){
      todoscpcrellenados = todoscpcrellenados+1;
    }
  }}

  if (result.value && todoscpcrellenados ==3) {
        sessionStorage.setItem('datos_cpc', result.value); //almacenar el importe del boton para pagos de clientes y otros gastos


    swal({
      title: 'Bien Hecho!',
      html:
        'Tus respuestas: <pre>' +
          JSON.stringify(result.value) +
        '</pre>',
      confirmButtonText: 'Confirmar!'
    })

    if ($("#tarjeta_resumen").is(':visible')){
    $('#boton_buscar').trigger('click');
    }
  }
  else{

    swal({
  position: 'top-end',
  type: 'error',
  title: 'Debes rellenar todos los datos',
  showConfirmButton: false,
  timer: 1800
}) // fin swal en else
$("#id_conectas").val('Sin Conecta Pymes');
} //fin else (si no ha rellenado todo)

})


} // fin if elegido = cpc
//Si tarjeta resumen ya está visible click en generar
if ($("#tarjeta_resumen").is(':visible') && conecta_elegido.substring(0,3)!='CPC'){
$('#boton_buscar').trigger('click');
}
}); //fin event change select

// FIN MODIFICAR SELECT DE CONECTA PYME
//-------------------------------------------





//-------------------------------------------*-----------------------------------------------------
//ACTIVAR GENERAR SI RESUMEN VISIBLE: MODIFICACIONES EN LOS SELECT SI EL DIV RESUMEN ESTÁ VISIBLE:
//-------------------------------------------*-----------------------------------------------------
//es decir, si la tarjeta resumen ya está activa, cualquiera de los cambios que haga que se muestren (clickar botón generar)

//1)PARA LOS TERMINALES MULTILINEA
$(document).on('change', "select[id*='id_terminales']", function(){
  if ($("#tarjeta_resumen").is(':visible')){
  $('#boton_buscar').trigger('click');
  }
});
//1)PARA LOS TERMINALES IEW
$(document).on('change', "select[id*='id_terminales_iew']", function(){
  if ($("#tarjeta_resumen").is(':visible')){
  $('#boton_buscar').trigger('click');
  }
});
//1)PARA SELECT DE VAP
$(document).on('change', "select[id*='id_vap']", function(){
  if ($("#tarjeta_resumen").is(':visible')){
  $('#boton_buscar').trigger('click');

  }
});
//1)PARA SELECT DE MFO
$(document).on('change', "select[id*='id_mfo']", function(){
  if ($("#tarjeta_resumen").is(':visible')){
  $('#boton_buscar').trigger('click');

  }
});

//1)PARA SELECT DE CV
$(document).on('change', "select[id*='id_cv']", function(){
  if ($("#tarjeta_resumen").is(':visible')){
  $('#boton_buscar').trigger('click');

  }
});

//1)PARA SELECT DE datos
$(document).on('change', "select[id*='id_voz_datos']", function(){
  if ($("#tarjeta_resumen").is(':visible')){
  $('#boton_buscar').trigger('click');
  }
});
//1)PARA SELECT DE origen
$(document).on('change', "select[id*='id_origen']", function(){
  if ($("#tarjeta_resumen").is(':visible')){
  $('#boton_buscar').trigger('click');
  }
});
//1)PARA SELECT DE NUMERO DE LÍNEAS
$(document).on('change', "input[id*='id_n_altas']", function(){
  if ($("#tarjeta_resumen").is(':visible')){
  $('#boton_buscar').trigger('click');
  }
});
//1)PARA SELECT DE TARIFA --> COMO YA HAY UN SELECT DE TARIFA PARA CHECKEAR SI ES IEW PRO O NO, LO PONGO EN ESA FUNCIÓN
//PARA SELECT DE CONECTA PYMES TB ESTÁ HECHO ARRIBA
// --------------------------------FIN CAMBIAR SELECT Y ACTUALIZAR GENERAR------------------------------------------------




//-------------------------------------------*-----------------------------------------------------
//BOTON INFO EQUIPOS + AJAX!!!!
//-------------------------------------------*-----------------------------------------------------
$(document).on('click', ".btnpequejorge2", function(e){


//obtener qué botón estoy pulsando
// ----------------------------------
var idClicked = e.target.id.slice(-1);


//obtener el terminal que quiero buscar la información.
// -----------------------------------------------------
if (idClicked==0){
  if ($("#id_terminales").is(':visible')){ //significa que es multilínea
    var terminal =$("#id_terminales" + " option:selected" ).text();
  } //fin si es multilínea
  else{
    var terminal =$("#id_terminales_iew" + " option:selected" ).text();
  }
} //fin id clicked ==0
else{ //el id no es cero
if ($("#id_terminales"+idClicked).is(':visible')){ //significa que es multilínea
  var terminal =$("#id_terminales"+idClicked + " option:selected" ).text();
} //fin si es multilínea
else{
  var terminal =$("#id_terminales_iew"+idClicked + " option:selected" ).text();
}
} //fin else si el id no es cero


//vamos al async (AJAXXXXX)
$.ajax({
  url: 'obtener_info_equipo_ajax',
  data: {
    'modelo':terminal
  },
  dataType: 'json',

  //si hay exito.....
  success: function(data) {

    //obtener los datos
    var info = data['info']
    var foto = data['foto']

    //hacer el swal
    swal({
  title: terminal,
  // text: info,
  html: '<font size="2">' + info + '</font>',
  imageUrl: '/' + foto,
  imageWidth: 300,
  imageHeight: 250,
  imageAlt: terminal,
  animation: false
}) //fin swal




  }//fin successful

});//FIN AJAXXXXX



}); //fin click button tip info




//-------------------------------------------*-----------------------------------------------------
//BOTON GUARDAR OPERACIÓN EN BASE DE DATOS!!!!!
//-------------------------------------------*-----------------------------------------------------

$('#boton_guardar').click(function(){
var filas_generadas = $("#principal").children().length;

console.log('mamon');
console.log(datostraidosdedjando);

//si la tarjeta resumen no está mostrada, no le he dado a generar
if ($("#tarjeta_resumen").is(':visible')){



swal({
  title: 'Guardar Operación',
  html:
    'Razón Social<input id="swal-input1" class="swal2-input">' +
    'CIF/NIF<input id="swal-input2" class="swal2-input">',
  focusConfirm: false,
  preConfirm: function () {
    return new Promise(function (resolve) {
      resolve([
        $('#swal-input1').val(),
        $('#swal-input2').val()
      ]) //fin resolve
    }) //fin promise. ni puta idea
  } //fin preconfirm


}).then(function (result) { //esto obtiene el resultado
  swal(JSON.stringify(result))



//SI SE HA RELLENADO AL MENOS LA RAZÓN SOCIAL
if (result['value'][0]){
  //Almacenar los datos en session
  sessionStorage.setItem('datos_guardar_razon_social', result['value'][0]); //almacenar razón social
  sessionStorage.setItem('datos_guardar_cif', result['value'][1]); //almacenar cif/nif
  var cif = result['value'][1];




  //la longitud del cif debe ser de 9 dígitos:
  if (cif.length!=9){
        swal({
        position: 'top-end',
        type: 'error',
        title: 'El CIF debe ser de 9 carácteres',
        showConfirmButton: false,
        timer: 1500
      });
  } //fin la longitud del cif debe ser de 9 digits

  //ajax para guardar los datos_cpc
  //vamos al async (AJAXXXXX)
  $.ajax({
    url: 'guardarConfiBD',
    data: {
      'razon_social':result['value'][0],
      'cif_nif':result['value'][1],
      'lineas_configuradas':lineas,
      'lineas_rentabilidad':datostraidosdedjando,
      'total_lineas':total_lineas,
      'filas':filas_generadas

    },
    dataType: 'json',

    //si hay exito.....
    success: function(datosbd) {



    if (datosbd['resultado']=='guardado_correctamente'){
          //hacer el swal
          swal({
          position: 'top-end',
          type: 'success',
          title: 'Your work has been saved',
          showConfirmButton: false,
          timer: 1500
        }) //fin swal
    }



    }//fin successful

  });//FIN AJAXXXXX



} //fin if (si se ha rellenado la razón social)
else{
          swal({
          position: 'top-end',
          type: 'error',
          title: 'Debes rellenar la razón social',
          showConfirmButton: false,
          timer: 1500
        })

} //fin else...debes rellenar al menos la razón social


})


} //fin si la tarjeta resumen SI está mostrad
else{ //SI LA TARJETA RESUMEN NO ESTÁ MOSTRADA
    swal({
    position: 'top-end',
    type: 'error',
    title: 'Debes generar la operación primero',
    showConfirmButton: false,
    timer: 1500
  })

}
}) //fin boton click
