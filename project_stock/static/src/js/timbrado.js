function alertar(){
                           var aux = document.getElementsByClassName("oe_form_char_content")[1].innerHTML.split("-");
                           var ruc = aux[0];
                           var dv = aux[1];
                           var timbrado = document.getElementById("oe-field-input-22").value;
                           var fecha = document.getElementsByName("date_invoice")[0].value;
                           var establecimiento = document.getElementById("oe-field-input-27").value;
                           var puntoExpedicion = document.getElementById("oe-field-input-28").value;
                           var numeroSecuencia = document.getElementById("oe-field-input-29").value;
                            var urlEset = "http://servicios.set.gov.py/EsetApiWSClient/?ruc" + ruc + "&digitoV=" + dv;

                           var myWindow = window.open(urlEset, "Header",
                           'width=1020,height=600,toolbar=no,resizable=yes,scrollbars=yes,menubar=no');

                           myWindow.focus();
                          // alert ("Ruc: "+ruc + "\ndv: "+dv + "\nTimbrado: " + timbrado + "\nfecha: "+fecha +
                           //"\nFactura: " + establecimiento + "-"+ puntoExpedicion + "-"+ numeroSecuencia);

                    }
function generar_reporte(nombre_reporte) {
    /**
     * Created by gcc on 02/11/16.
     */
    var host = "http://chacore.com.py:8080";
    var tiene_iva = false;
    var url;
    var meses = document.getElementById("mes");
    if (meses != null){
        var mes = meses.options[meses.selectedIndex].value;
        var periodo = document.getElementById("periodo").value;
    }
    var tipos = document.getElementById("tipo_archivo");
    var tipo_archivo =  tipos.options[tipos.selectedIndex].value;
    var monedas = document.getElementById("moneda");
    if (monedas != null){
            var moneda =  monedas.options[monedas.selectedIndex].value;

    }
    var reportes = document.getElementById("tipo_reporte");
    if (reportes != null){
        var tipo_reporte = reportes.options[reportes.selectedIndex].value;
    }

    if ($("#tiene_iva").is(':checked')) {
        tiene_iva = true
    }else {
        tiene_iva = false
    }
    //alert(periodo+" "+mes + " "+ tipo_archivo);
   // alert ('\nNOmbre del reporte:'+nombre_reporte+ '\nMes:'+mes+' \nPeriodo:'+periodo +'\nTipo de archivo: ' + tipo_archivo);
    if (nombre_reporte == 'compras'){

	     url = host+'/jasperserver/flow.html?_flowId=viewReportFlow&_flowId=viewReportFlow&ParentFolderUri=%2FReportes_Odoo&reportUnit=%2FReportes_Odoo%2FLibro_Compras&standAlone=true&j_username=jasperadmin&j_password=jasperadmin' +
        '&ACCOUNT_PERIOD='+periodo+"&ACCOUNT_MONTH="+mes+"&MONEDA="+moneda+"&output="+tipo_archivo;



         //console.log(centro_de_costo);
    }else if (nombre_reporte == 'ventas'){
         url = host+'/jasperserver/flow.html?_flowId=viewReportFlow&_flowId=viewReportFlow&ParentFolderUri=%2FReportes_ODOO&reportUnit=%2FReportes_ODOO%2Fventas&standAlone=true&j_username=jasperadmin&j_password=jasperadmin' +
        '&ACCOUNT_PERIOD='+periodo+"&ACCOUNT_MONTH="+mes+"&output="+tipo_archivo;

       // url = 'http://190.112.210.198:8080/jasperserver/flow.html?_flowId=viewReportFlow&standAlone=true&_flowId=viewReportFlow&ParentFolderUri=%2FReportes_ODOO&reportUnit=%2FReportes_ODOO%2FLIbro&j_username=jasperadmin&j_password=jasperadmin' +
        //'&ACCOUNT_PERIOD='+periodo+"&ACCOUNT_MONTH="+mes+"&output="+tipo_archivo;
    } else if (nombre_reporte == 'chechauka'){
        url = host+'/jasperserver/flow.html?_flowId=viewReportFlow&_flowId=viewReportFlow&ParentFolderUri=%2FReportes_Odoo&reportUnit=%2FReportes_Odoo%2Fhechauka_compras&standAlone=true&j_username=jasperadmin&j_password=jasperadmin' +
        '&ACCOUNT_PERIOD='+periodo+"&ACCOUNT_MONTH="+mes+"&TYPE="+tipo_reporte+"&output="+tipo_archivo;
    }  else if (nombre_reporte == 'vhechauka'){
        url = host+'/jasperserver/flow.html?_flowId=viewReportFlow&_flowId=viewReportFlow&ParentFolderUri=%2FReportes_Odoo&reportUnit=%2FReportes_Odoo%2Fhechauka_ventas&standAlone=true&j_username=jasperadmin&j_password=jasperadmin' +
        '&ACCOUNT_PERIOD='+periodo+"&ACCOUNT_MONTH="+mes+"&TIPO="+tipo_reporte+"&output="+tipo_archivo;
    }  else if (nombre_reporte == 'compras_proveedor') {
        var user = $(".oe_form_char_content").html();
        var estados_aux = [];
            $('#estados input:checked').each(function() {
                estados_aux.push($(this).attr('name'));
            });
        var proveedor = $(".ui-autocomplete-input").val().trim();
        //var desde = $("input[name='desde']").val().replace("/"," ").replace("."," ");
        var desde_aux = $("input[name='desde']").val();
        var hasta_aux = $("input[name='hasta']").val();
        // desde = transformarFecha(desde);
        var desde = transformarFecha(desde_aux);
        var hasta = transformarFecha(hasta_aux);
        var i;
        var estados = "";
            for (i = 0; i < estados_aux.length; ++i) {
                console.log(estados_aux[i]);
                estados += "'".concat(estados_aux[i]).concat("\'").concat(",").trim();
                console.log(estados);
            }
        estados = estados.slice(',', -1).trim();
        console.log("Desde:" + desde + "\nHasta:" + hasta + "\nProveedor:" + proveedor+"\nEstados:"+estados);
         url = host+'/jasperserver/flow.html?_flowId=viewReportFlow&standAlone=true&_flowId=viewReportFlow&ParentFolderUri=%2FReportes_ODOO&reportUnit=%2FReportes_ODOO%2FCOMPRAS_PROVEEDOR&j_username=jasperadmin&j_password=jasperadmin' +
        '&DESDE='+desde+"&HASTA="+hasta+"&PROVEEDOR="+proveedor+"&STATES="+estados+"&USER="+user+"&output="+tipo_archivo;
         url = url.trim();
        console.log(url);
    } else if (nombre_reporte == 'compras_costos') {
           /* odoo.define('reports.costos.timbrado_js', function(require) {
                "use strict";
                var Model = require('web.Model');
                (new Model('your.model')).call('your_function').then(function (res) {
                    console.log(res);
                });

            });*/
        var user = $(".oe_form_char_content").html();
        var estados_aux = [];
            $('#estados input:checked').each(function() {
                estados_aux.push($(this).attr('name'));
            });
        //var desde = $("input[name='desde']").val().replace("/"," ").replace("."," ");
        var desde_aux = $("input[name='desde']").val();
        var hasta_aux = $("input[name='hasta']").val();
        // desde = transformarFecha(desde);
        var desde = transformarFecha(desde_aux);
        var hasta = transformarFecha(hasta_aux);
        var i;
        var estados = "";
            for (i = 0; i < estados_aux.length; ++i) {
                console.log(estados_aux[i]);
                estados += "\'".concat(estados_aux[i]).concat("\'").concat(",").trim();
                console.log(estados);
            }
        estados = estados.slice(',', -1).trim();
        var centro_de_costo = retornarCostos();
        console.log("Desde:" + desde + "\nHasta:" + hasta +"\nEstados:"+estados+"\nCentros de costos:"+centro_de_costo);
         url = host+'/jasperserver/flow.html?_flowId=viewReportFlow&standAlone=true&_flowId=viewReportFlow&ParentFolderUri=%2FReportes_ODOO&reportUnit=%2FReportes_ODOO%2FCOMPRAS_COSTOS&j_username=jasperadmin&j_password=jasperadmin' +
        '&DESDE='+desde+"&HASTA="+hasta+"&COSTOS="+centro_de_costo+"&STATES="+estados+"&USER="+user+"&output="+tipo_archivo;
         url = url.trim();
        console.log(url);
    }
    var myWindow=window.open(url);
}

function chequeo() {
    if ($("#seleccion").is(':checked')) {
            $(".oe_form_many2many_checkboxes input[type=checkbox]").each(function () {
                $(this).prop("checked", true);
            });

        } else {
            $(".oe_form_many2many_checkboxes input[type=checkbox]").each(function () {
                $(this).prop("checked", false);
            });
        }
}
function radio() {
    if ($("#tiene_iva").is(':checked')) {
            $(".oe_form_many2many_checkboxes input[type=checkbox]").each(function () {
                $(this).prop("disabled", true);
                $(this).prop("checked", false);
            });
            $("#seleccion").prop("disabled", true)

        } else {
            $(".oe_form_many2many_checkboxes input[type=checkbox]").each(function () {
                $(this).prop("disabled", false);
            });
            $("#seleccion").prop("disabled", false)
        }
}
function controlarIVA(){
    var contiene = false;
    if ($("#tiene_iva").is(':checked')) {
            contiene = true;
    }
    return contiene
}

function retornarCostos(){
     var centro_de_costo ="  ";
     $('input[type=checkbox]').each(function () {
                if ($(this).parents('.oe_form_many2many_checkboxes').length) {
                    if($(this).is(':checked')) {
                        aux = $(this)[0].nextSibling.nodeValue.trim();
                        centro_de_costo += "\'".concat(aux).concat("\'").concat(",").trim();

                    }
                }
             //var sThisVal = (this.checked ? $(this).val() : "");
         });
         centro_de_costo = centro_de_costo.slice(',', -1).trim();
         return centro_de_costo
}

function transformarFecha(fecha_original){
    var fecha = "";
    var enero = "ene.";
    var febrero = "feb.";
    var marzo = "mar.";
    var abril = "abr.";
    var mayo = "may.";
    var junio = "jun.";
    var julio = "jul.";
    var agosto = "ago.";
    var septiembre = "sep.";
    var octubre = "oct.";
    var noviembre ="nov.";
    var diciembre ="dic.";
    if (fecha_original.includes(enero)){
        fecha = fecha_original.replace(enero,"01");
    }
    if (fecha_original.includes(febrero)){
        fecha = fecha_original.replace(febrero,"02");
    }
    if (fecha_original.includes(marzo)){
        fecha = fecha_original.replace(marzo,"03");
    }
    if (fecha_original.includes(abril)){
        fecha = fecha_original.replace(abril,"04");
    }
    if (fecha_original.includes(mayo)){
        fecha = fecha_original.replace(mayo,"05");
    }
    if (fecha_original.includes(junio)){
        fecha = fecha_original.replace(junio,"06");
    }
    if (fecha_original.includes(julio)){
        fecha = fecha_original.replace(julio,"07");
    }
    if (fecha_original.includes(agosto)){
        fecha = fecha_original.replace(agosto,"08");
    }
    if (fecha_original.includes(septiembre)){
        fecha = fecha_original.replace(septiembre,"09");
    }
    if (fecha_original.includes(octubre)){
        fecha = fecha_original.replace(octubre,"10");
    }
    if (fecha_original.includes(noviembre)){
        fecha = fecha_original.replace(noviembre,"11");
    }
    if (fecha_original.includes(diciembre)){
        fecha = fecha_original.replace(diciembre,"12");
    }
    fecha = fecha.replace('/','-');
    fecha = fecha.replace('/','-');
    fecha = fecha.replace('/','-');

    return fecha;
}



