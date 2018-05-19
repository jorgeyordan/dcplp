from django.shortcuts import render
from .import views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib import auth
from django.views import View
from confi.models import TerminalesMaestro
from confi.models import OT_multi_hasta20, OT_iew_sub, OT_multi_vap, OT_iew_vap, OT_multi_desde20, Comisiones_conecta, Comisiones_conecta, TerminalesMaestro, Comisiones_prima_operaciones,OperacionesConfiGuardadas
from confi.models import Comisiones_iew
from confi.models import Comisiones_datos
from confi.models import Comisiones_multilinea
import json
from django.http import HttpResponse
import math
from django.db.models import Count
from django.views.generic.detail import DetailView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import csv
import xlwt
import datetime




@login_required
def index(request):
    username = request.user.username
    # tabla = valores_unicos.filter(usuario=username)
    # tabla = OperacionesConfiGuardadas.objects.order_by('razon_social').values('razon_social').distinct()
    # tabla =  OperacionesConfiGuardadas.objects.all().filter(usuario=username)
    tabla =OperacionesConfiGuardadas.objects.raw("SELECT * FROM confi_operacionesconfiguardadas WHERE usuario ='"+ username + "' GROUP BY razon_social") #el raw funciona pero no el paginator


    page = request.GET.get('page', 1)
    paginator = Paginator(list(tabla),10) #numero de registros por página #lo normal es que sea sin la función list. pero se utiliza al ser un raw queryset

    try:
        listado = paginator.page(page)
    except PageNotAnInteger:
        listado = paginator.page(1)
    except EmptyPage:
        listado = paginator.page(paginator.num_pages)

    #conseguir list of dicts para graph js

    fields =[]
    data=[]

    for item in tabla:
        fields.append(item.razon_social)
        data.append(item.total_lineas)

    print(request.user.groups.filter(name='director').exists())
    print(request.user.get_group_permissions)

    return render(request, 'index.html', {'usuario':username, 'tabla':listado, 'data':data, 'fields':fields} )



#
# class OperacionesView(DetailView):
#     model = OperacionesConfiGuardadas
#
#     template_name = 'detalle_operacion.html'


@login_required
def terminales_ranking(request):
    username = request.user.username
    return render(request, 'terminales.html', {'usuario':username} )



@login_required
def confi_multilinea(request):
    terminalesOT = OT_multi_hasta20.objects.all().order_by('modelo')
    iewOT = OT_iew_sub.objects.all()
    conectas = Comisiones_conecta.objects.all()
    return render(request, 'confi_multilinea.html', {'terminales':terminalesOT, 'terminales_iew':iewOT, 'conectas':conectas} )


# VISTA AJAX CONFIGURADOR RENTABILIDAD DE LAS LÍNEAS
# ---------------------------------------------------
@login_required
def configurador_ajax_view(request):
    '''RESUMEN DE ESTA FUNCIÓN QUE EMPIEZA A SER MUY LARGA
    1)se incicializan algunas variables y arrays
    2)se obtienen los datos enviados por ajax, (moviles, conecta, cpc, etc)
    2.5) se calcula prima de volumen fijo
    3) se hacen algunos cálculos para obtener: total lineas, oficina plus, cabeceras, agentes, cliente valor
    4) se calcula la prima de OPERACIONES
    5)se calcula si es cliente valor (volumen)
    6) SE HACE LOOP POR CADA UNA DE LAS FILAS CONFIGURADAS PARA:
        6.1 - en función de la tarifa se define en qué columna buscar para el dxc
        6.2 - se obtiene precio de cesión, dxc y gama
        6.3 - se obtiene comisinoes básicas (voz, datos, extra, sva)
        6.4 - se obtienen otros datos como gama_jorge y el nombre de la foto
        6.5 - se calcula la prima de volumen
        6.6 - se obtienen las RECOMENDACIONES. (esto es largo porque se hacen varia en función de la tarifa y el modelo de subvencion)
    7)todas las variables se meten en array y se devuelven como jason mediante ajax
    '''

    # definir los arrays que voy a utilizar:
    valores =[]
    avisos = ""
    array_devuelto = []
    data = {}
    lineasoperacion=0
    numero_cabeceras = 0
    numero_centralitas = 0
    numero_lineas_multilinea = 0
    numero_lineas_negocio_u_oficina = 0
    numero_lineas_iew = 0
    conecta_valor_volumen =False
    esclientevalor = False #valor para prima de volumen
    esclienteOficinaPlus = False
    comision_volumen = 0
    grupo_usuario = 'otro'


    #ESTO para saber si debo mostrar o no las primas (se pasa a jquery por lo que cuidado)
    #si el usuario está en el grupo "comercial" no debería mostrar nada
    if (request.user.groups.filter(name='comercial').exists()):
        grupo_usuario = 'comercial'

    #obtener en un array todos los valores enviados por la pagina.
    #estas dos lineas es cómo lo tenía antes.
    # for i in request.GET: #obtener array de dos dimensiones
    #   valores.append(request.GET.getlist(i)) #lineas3 = request.GET.getlist("datos[]") (si fuera un array nomral este me valdría. )

    #obtengo el querydict (esto es, todo lo que me devuelve ajax)
    # --------------------
    q = request.GET
    l = len(q) #el último el la key del conecta (este no hay que cogerlo)


    #obtener los datos de CPC
    datos_cpc = q.get('cpc')
    if datos_cpc !='sin_cpc':
        esclientevalor = True
        n_comunicator = int(datos_cpc.split(',')[0])
        n_puestos_simples = int(datos_cpc.split(',')[1])
        n_puestos_avanzados = int(datos_cpc.split(',')[2])

        comision_cpc_comunicator = n_comunicator *25
        comision_cpc_simple = n_puestos_simples * 20
        comision_cpc_avanzado = n_puestos_avanzados* 85

    else:
        comision_cpc_comunicator = 0
        comision_cpc_simple = 0
        comision_cpc_avanzado = 0
        n_comunicator = 0
        n_puestos_simples = 0
        n_puestos_avanzados = 0


    #obtener los datos de Conecta Pyme
    conecta_elegido = q.get('conecta')
    if conecta_elegido =='Sin Conecta Pymes':
        esclientevalor = False
        comision_conecta = 0
        columna_prima_operaciones = 'comision_operaciones_0'
        columna_prima_operaciones_oficina_plus = 'comision_operaciones_0'
    else:
        fila = Comisiones_conecta.objects.values().filter(conecta=conecta_elegido)
        conecta_valor_volumen = Comisiones_conecta.objects.values().filter(conecta=conecta_elegido)[0]['valor_volumen']
        comision_conecta =  fila[0]['comision'] + comision_cpc_comunicator + comision_cpc_simple + comision_cpc_avanzado
        columna_prima_operaciones = Comisiones_conecta.objects.values().filter(conecta=conecta_elegido)[0]['columna_prima_operaciones']
        columna_prima_operaciones_oficina_plus = Comisiones_conecta.objects.values().filter(conecta=conecta_elegido)[0]['columna_prima_operaciones_oficina_plus']

    if (n_puestos_simples + n_puestos_avanzados)>=4 and(esclienteOficinaPlus==False):
        columna_prima_operaciones = 'acelerador_conecta_1'



    #obtener en un array todas las líneas móviles
    for i in range(l):
        valores.append(q.getlist('datos['+str(i)+'][]'))


    #1.0.1) -->obtener el total de líneas configuradas, líneas multilínea, pinchos y de qué tipo...etc
    for i in range(len(valores)-2): #por cada una de las líneas....
        lineasoperacion = lineasoperacion + int(valores[i][0]) #sumar cuantas líneas hay
        if valores[i][4] =='cabecera': #si es cabecera, añadir uno
            numero_cabeceras = numero_cabeceras + int(valores[i][0])
        elif valores[i][4] =='agente': # si es agente, contar cabeceras
            numero_centralitas = numero_centralitas + int(valores[i][0])

        if valores[i][1]=='optima' or valores[i][1]=='optima_rpv' or valores[i][1]=='solper':
            numero_lineas_multilinea = numero_lineas_multilinea + int(valores[i][0])
        else: #debe ser iew no?
            numero_lineas_iew = numero_lineas_iew + int(valores[i][0])
            if valores[i][1]=='4gnegocio' or valores[i][1]=='4goficina':
                numero_lineas_negocio_u_oficina = numero_lineas_negocio_u_oficina + int(valores[i][0])




    if numero_cabeceras>0 and numero_centralitas>=2:
        esclienteOficinaPlus = True

    tamano_pago_operaciones = numero_lineas_multilinea- numero_cabeceras
    if tamano_pago_operaciones >40:
        tamano_pago_operaciones=40

    #PRIMA OPERACIONES!!!!!-----------------------------------------
    # SI ES UN CLIENTE DE MÁS DE 10
    if tamano_pago_operaciones >=10:

        #Obtener la comisión base:
        # ---------------------------
        comision_base_operaciones = Comisiones_prima_operaciones.objects.values().filter(tamaño_pago=tamano_pago_operaciones)[0]['base']



        #obtener el acelerador de convergencia!
        # ---------------------------
        if esclienteOficinaPlus == True:
            columna_a_buscar_acelerador_conecta = columna_prima_operaciones_oficina_plus
        else:
            columna_a_buscar_acelerador_conecta = columna_prima_operaciones

        comision_acelerador_convergencia = Comisiones_prima_operaciones.objects.values().filter(tamaño_pago=tamano_pago_operaciones)[0][columna_a_buscar_acelerador_conecta]


        #obtener el acelerador de iew pro!
        # ---------------------------

        if (numero_lineas_iew>=1) and (numero_lineas_iew<=3):
            columna_a_buscar_acelerador_iew = 'acelerador_iew_pro_3'

        elif (numero_lineas_iew>=4) and (numero_lineas_iew<=9):
            columna_a_buscar_acelerador_iew = 'acelerador_iew_pro_2'

        elif (numero_lineas_iew>=10):
            columna_a_buscar_acelerador_iew = 'acelerador_iew_pro_1'

        else:
            columna_a_buscar_acelerador_iew = 'comision_operaciones_0'

        comision_acelerador_iew = Comisiones_prima_operaciones.objects.values().filter(tamaño_pago=tamano_pago_operaciones)[0][columna_a_buscar_acelerador_iew]

    else:
        comision_base_operaciones = 0
        comision_acelerador_convergencia = 0
        comision_acelerador_iew = 0



    #si no tiene líneas móviles, tiene cpc, tiene también un acelerador...
    # ------------------------------------------------
    if (lineasoperacion==0) and (datos_cpc !='sin_cpc'):
        if esclienteOficinaPlus == False:
            if n_puestos_avanzados>=2 and n_puestos_avanzados<=4:
                comision_acelerador_convergencia = 180
            if n_puestos_avanzados>=5 and n_puestos_avanzados<=9:
                comision_acelerador_convergencia = 216


    #obtener si es cliente valor por líneas y servicios (cpc está en otro apartado y cp digital en otro (tres apartados))
    if lineasoperacion>=10:
        esclientevalor = True
    elif lineasoperacion>=5:
        if numero_cabeceras>0 and numero_centralitas>=2:
            esclientevalor = True
        if conecta_valor_volumen ==True:
            esclientevalor = True



    #2.5-obtener la prima de volumen fijo

    if (conecta_valor_volumen == True) and (esclientevalor == True):
        prima_volumen_fijo = comision_conecta * 0.35
    else:
        prima_volumen_fijo = 0

    #---------------------------------------------------------
    # 1) --> LOOP: BUCLE POR TODOS LOS ELEMENTOS DEL ARRAY: OBTENIENDO (nlineas, navegaiones, dxc, comisiones etc)
    for i in range(len(valores)-2):
        avisos = ''
        #obtener los valores
        unidades = valores[i][0]
        tarifa = valores[i][1]
        origen = valores[i][2]
        navegacion  = valores[i][3]
        cv  = valores[i][4]
        mfo  = valores[i][5]
        vapsub =valores[i][6]
        terminal = valores[i][7]
        linea_sin_dxc = False
        terminal_vap_reco_sobre_cliente = False






        #1.1) -->EN FUNCIÓN DEL PAQUETE DE DATOS, ASIGNAR Nº DE COLUMNA
        #si es multilínea:
        if tarifa=='optima' or tarifa=='optima_rpv' or tarifa=='solper':
            grupo_tarifa = 'multi'

            if navegacion == 'sin_datos':
                columna = 1
            elif navegacion == '1gb':
                columna = 1
            elif navegacion == '2gb':
                columna = 2
            elif navegacion == '5gb':
                columna = 3
            elif navegacion == '12gb':
                columna = 4
            elif navegacion == '30gb':
                columna = 5

        else: #es iew
            grupo_tarifa = 'iew'

            if tarifa == '4gnegocio':
                columna = 3
            if tarifa == '4goficina':
                columna = 4
            if tarifa == 'iew10':
                columna = 3
            if tarifa == 'iew8':
                columna = 2
            if tarifa == 'iew3':
                columna = 1

        #1.2) -->SE CONSIDERA CAPTA O PORTA (ORIGEN) (1 para terminales, 2 para comision)
        if origen == 'Postpago':
            capta_porta = 'porta'
            capta_porta2 = 'porta'
        elif origen == 'Prepago':
            capta_porta = 'porta'
            capta_porta2 = 'capta'
        elif origen == 'Captación':
            capta_porta = 'capta'
            capta_porta2 = 'capta'
        elif origen == 'Migración':
            capta_porta = 'capta'
            capta_porta2 = 'capta'


        #1.3) -->OBTENER PRECIO CESIÓN, DXC Y GAMA
        #*********************************************************************
        #primero, SI ES MULTILÍNEA----------------------------------
        if grupo_tarifa=='multi':

            #es más de 20 o menos de 20?
            if lineasoperacion <=20:
                fila = OT_multi_hasta20.objects.values().filter(modelo=terminal)
            else:
                fila = OT_multi_desde20.objects.values().filter(modelo=terminal)

            #A) si es subvencionado:
            if vapsub=='no_vap':

                dxc = fila[0][capta_porta+str(columna)]
                precio = fila[0]['precio']
                gama = fila[0]['gama']
                pvp = 'flex'
                cuota = 'No aplica'

             # B)si es en vap
            else:
                fila = OT_multi_vap.objects.values().filter(modelo=terminal)
                if capta_porta =='porta':
                    dxc = fila[0]['dxc'+str(columna)]
                    precio = fila[0]['precio']
                    gama = fila[0]['gama']
                    pvp = fila[0]['pago'+str(columna)] #el pvp en subvencionado es pago cliente (por ejemplo pinchos, pero en vap es el pago inicial)
                    cuota = fila[0]['cuota'+str(columna)]
                    if cuota =='-':
                        avisos = avisos + "No está permitido vender este terminal con ese paquete de voz y datos en venta a plazos.  "
                else:
                    avisos = avisos + "Venta a plazos en capta solo es posible pago único.  "
                    dxc = fila[0]['dxc_pago_unico']
                    precio = fila[0]['precio']
                    gama = fila[0]['gama']
                    pvp = fila[0]['pago_unico_capta']
                    cuota = 0
                    if pvp ==0:
                        avisos = avisos + " No se puede configurar este modelo en venta a plazos.  "



        #Si es iew
        else:
            #A) si es subvencionado:
            if vapsub=='no_vap':
                fila = OT_iew_sub.objects.values().filter(modelo=terminal)
                dxc = fila[0]['dxc'+str(columna)]
                precio = fila[0]['precio']
                gama = fila[0]['gama']
                pvp = fila[0]['precio'+str(columna)]
                cuota = 'No Aplica'
            # B)si es en vap
            else:

                if capta_porta =='porta':
                    fila = OT_iew_vap.objects.values().filter(modelo=terminal)
                    dxc = fila[0]['dxc'+str(columna)]
                    precio = fila[0]['precio']
                    gama = fila[0]['gama']
                    pvp = fila[0]['pago'+str(columna)]
                    cuota = fila[0]['cuota'+str(columna)]
                else:
                    fila = OT_iew_vap.objects.values().filter(modelo=terminal)
                    dxc = fila[0]['dxc_pago_unico']
                    precio = fila[0]['precio']
                    gama = fila[0]['gama']
                    pvp = fila[0]['pago_unico_capta']
                    cuota = 0
                    avisos = avisos + "Las ventas a plazos que no sean portabilidades sólo se pueden realizar mediante pago único.  "



        #1.4) -->si el terminal no es voz ni fixed y va sin datos, el dxc será cero
        if (navegacion == 'sin_datos') and  grupo_tarifa == 'multi':
            if (gama!='VOZ') and  (gama!='FIX') and (terminal!='sin_terminal'):
                dxc=0
                avisos = avisos + "No se debe configurar este modelo sin datos!.  "
                linea_sin_dxc = True


        #si es un fixed con más de 2gb no se puede vender!!
        if gama == 'FIX' and columna > 2:
            avisos = avisos + "No es posible ofertar un Fixed con ese paquete de datos!"


        #1.5) -->obtener el valor de la comision de voz
        if grupo_tarifa=='multi': # 1.5.1) -->si es multilínea:
            fila_voz = Comisiones_multilinea.objects.values().filter(tarifa=tarifa)
            com_voz = fila_voz[0][capta_porta2]
        else:# 1.5.1) -->si es iew:
            if lineasoperacion < 10:
                fila_voz = Comisiones_iew.objects.values().filter(tarifa=tarifa)
                com_voz = fila_voz[0]['com1_9']
            else:
                fila_voz = Comisiones_iew.objects.values().filter(tarifa=tarifa)
                com_voz = fila_voz[0]['com10']




        #obtener el valor de la comision de datos
        if navegacion == 'sin_datos':
            com_datos = 0
        else:
            fila_datos = Comisiones_datos.objects.values().filter(id=columna)
            com_datos = fila_datos[0]['comision']

        #obtener el varlod de la comision extraterimanl
        if (gama=='SPH-4G') or (gama=='VOZ'):
            com_extra = fila_voz[0]['terminal_movil_'+capta_porta2]
        else:
            com_extra = 0

        #obtener la comision de SVA
        if (cv=='agente'):
            com_cv = 10
        else:
            com_cv=0
        if (mfo=='mfo_porta') and (int(unidades)>=10):
            com_mfo = 15
        else:
            com_mfo=0
        com_sva = com_cv + com_mfo

        #si es una cabecera, todas las comisiones a cero
        if (cv=='cabecera'):
            com_cv=0
            com_extra=0
            com_voz = 0
            com_datos = 0

            if navegacion != 'sin_datos':
                avisos = avisos + "Una cabecera no debería llevar datos.  "
            if terminal !='sin_terminal':
                avisos = avisos + "Una cabecera no debería llevar terminal.  "


        #rentabilidad total de la línea:
        if not unidades:
            unidades = 0
        if unidades!=0:
            rent = int(com_voz) + int(com_datos) + int(com_extra) + int(com_sva) + int(dxc) - int(precio)


        else:
            rent =0
            avisos = avisos + "No has configurado nº de líneas.  "
        total = rent * int(unidades)



        #obtener el nombre de la foto y gama gama_jorge
        if grupo_tarifa=='multi':
            nombre_foto = OT_multi_hasta20.objects.values().filter(modelo=terminal)[0]['nombre_foto']
            gama_jorge = OT_multi_hasta20.objects.values().filter(modelo=terminal)[0]['gama_jorge']
        else:
            nombre_foto = OT_iew_sub.objects.values().filter(modelo=terminal)[0]['nombre_foto']
            gama_jorge = OT_iew_sub.objects.values().filter(modelo=terminal)[0]['gama_jorge']


        ##OBTENER LA PRIMA DE Volume--------------------------------
        if esclientevalor:
            if grupo_tarifa=='multi':
                comision_volumen = comision_volumen + ((com_voz + com_extra + com_datos)*0.7)*int(unidades)
            else:
                comision_volumen = comision_volumen + ((com_voz + com_extra + com_datos)*0.35)*int(unidades)


        #---------------------------------------------------------------------------
        # OBTENER LAS RECOMENDACIONES**************
        #---------------------------------------------------------------------------

        #SI ES MULTILÍNEA SUBVENCIONADO!!!
        #------------------------------------------------------------------------
        if grupo_tarifa=='multi' and vapsub=='no_vap':
            #obtener los intervalos de precio de cesión que busco
            if gama_jorge =='SPH':
                i_inferior = precio - (precio*0.05)
                i_superior = 2000
            else:
                i_inferior = precio - (precio*0.6)
                i_superior = 2000


            #obtener filtro con intervalos y de la misma gama
            if lineasoperacion <=20:
                reco_listado = OT_multi_hasta20.objects.filter(gama_jorge=gama_jorge ,precio__gte=i_inferior, precio__lte=i_superior).values()
            else:
                reco_listado = OT_multi_desde20.objects.filter(gama_jorge=gama_jorge ,precio__gte=i_inferior, precio__lte=i_superior).values()


            #por cada uno de los resultados obtener el dxc-precio
            reco_dif_actual = dxc-precio
            todosaqui= ''
            mgequipo = dxc-precio

            #Por cada uno de los terminales con precio mayor o 5% inferior:....
            for terminal_opcional in reco_listado:
                if linea_sin_dxc == False:
                    reco_dif = terminal_opcional[capta_porta+str(columna)] - terminal_opcional['precio'] #con esto obtendo el mg del equipo. negativo si precio>dxc
                else:
                    reco_dif = 0 - terminal_opcional['precio'] #con esto obtendo el mg del equipo. negativo si precio>dxc

                #cuánto añadimos a la rentabilidad de la línea si elegimos este otro????
                suma_rent   = math.fabs(mgequipo-reco_dif)

                #obviamente: solo si: el margen de la recomendación es mayor al elegido.....
                if reco_dif > reco_dif_actual:
                    todosaqui = todosaqui + '<li><b>'+terminal_opcional['modelo'] + '</b>(' + str(reco_dif) + ') Añade: + ' + str(math.fabs(suma_rent)) + '€</li>'

            #si no se ha definido todos aquí es que no hay ningún equipo que mejore la rentabilidad de esta línea
            if not todosaqui:
                todosaqui = 'Lo sentimos. No encontramos recomendaciones!'

            if terminal == 'sin_terminal':
                todosaqui = 'Sin terminal, no existen recomendaciones.'


        #SI ES MULTILÍNEA VENTA A PLAZOS!!!
        #------------------------------------------------------------------------
        if grupo_tarifa=='multi' and vapsub=='si_vap':
            if cuota ==0:
                cuota_vap_float = 0

            elif cuota !='-':
                #cuanto paga el cliente en vap. total (pvp + cuotas24)
                cuota_vap_float = float(cuota.replace(',','.'))
                cliente_vap_pago_total = int(pvp) + cuota_vap_float*24 #cuáto paga el cliente por el terminal que se ha elegido?

            #obtener los intervalos de precio de cesión que busco
            i_inferior = precio - (precio*0.05)
            i_superior = 2000

            #obtener filtro con intervalos y de la misma gama
            reco_listado = OT_multi_vap.objects.filter(gama_jorge=gama_jorge ,precio__gte=i_inferior, precio__lte=i_superior).values()

            #por cada uno de los resultados obtener el dxc-precio
            reco_dif_actual = dxc-precio
            todosaqui= ''
            mgequipo = dxc-precio

            #Por cada uno de los terminales con precio mayor o 5% inferior:....
            for terminal_opcional in reco_listado:

                #Si es una línea con margen = 0, no hay mucho que mejorar, entonces buscar pago total cliente
                if mgequipo == 0 and terminal_opcional['cuota'+str(columna)]!='-': #(nunca va a haber en vap un dxc mayor que el precio de cesión)
                    pago_cliente_vap_reco = int(terminal_opcional['pago'+str(columna)])
                    cuota_cliente_vap_reco  = float(terminal_opcional['cuota'+str(columna)].replace(',','.'))*24
                    cliente_vap_pago_total_reco = pago_cliente_vap_reco + cuota_cliente_vap_reco

                    #si lo que paga el cliente en reco es menor que lo que paga con el equipo elegido...
                    if cliente_vap_pago_total_reco<cliente_vap_pago_total:
                        terminal_vap_reco_sobre_cliente = True
                        mg_pago_total_actual_reco = cliente_vap_pago_total - cliente_vap_pago_total_reco
                        todosaqui = todosaqui + '<li><b>'+terminal_opcional['modelo']+' (paga en total ' + str("%.2f" % mg_pago_total_actual_reco) + '€ menos)</li></b>'

                else: #si el margen de equipo es negativo....
                    #obtener el margen de equipo del terminal a recomendar
                    reco_dif = terminal_opcional['dxc'+str(columna)] - terminal_opcional['precio']

                    if linea_sin_dxc == False:
                        reco_dif = terminal_opcional['dxc'+str(columna)] - terminal_opcional['precio'] #con esto obtendo el mg del equipo. negativo si precio>dxc
                    else:
                        reco_dif = 0 - terminal_opcional['precio'] #con esto obtendo el mg del equipo. negativo si precio>dxc

                    #cuánto añadimos a la rentabilidad de la línea si elegimos este otro????
                    suma_rent   = math.fabs(mgequipo-reco_dif)

                    #obviamente: solo si: el margen de la recomendación es mayor al elegido.....y además si es portabilidad porque si es capta en pago unico no se puede y ya me pierdo
                    if reco_dif > reco_dif_actual and capta_porta=='porta':
                        todosaqui = todosaqui + '<li><b>'+terminal_opcional['modelo'] + '</b>(' + str(reco_dif) + ') Añade: + ' + str(math.fabs(suma_rent)) + '€</li>'

            #si no se ha definido todos aquí es que no hay ningún equipo que mejore la rentabilidad de esta línea
            if not todosaqui:
                todosaqui = 'Lo sentimos. No encontramos recomendaciones!'

            if terminal == 'sin_terminal':
                todosaqui = 'Sin terminal, no existen recomendaciones.'



        #SI ES IEW SUBVENCIONADO!!!
        #------------------------------------------------------------------------
        if grupo_tarifa=='iew' and vapsub=='no_vap':
            i_inferior = precio - (precio*0.8)
            i_superior = 2000

            #obtener filtro con intervalos y de la misma gama
            reco_listado = OT_iew_sub.objects.filter(gama_jorge=gama_jorge ,precio__gte=i_inferior, precio__lte=i_superior).values()

            #por cada uno de los resultados obtener el dxc-precio
            reco_dif_actual = dxc-precio
            todosaqui= ''
            mgequipo = dxc-precio

            #Por cada uno de los terminales con precio mayor o 5% inferior:....
            for terminal_opcional in reco_listado:

                if linea_sin_dxc == False:
                    reco_dif = terminal_opcional['dxc'+str(columna)] - terminal_opcional['precio'] #con esto obtendo el mg del equipo. negativo si precio>dxc
                else:
                    reco_dif = 0 - terminal_opcional['precio'] #con esto obtendo el mg del equipo. negativo si precio>dxc

                #cuánto añadimos a la rentabilidad de la línea si elegimos este otro????
                suma_rent   = math.fabs(mgequipo-reco_dif)

                #obviamente: solo si: el margen de la recomendación es mayor al elegido.....
                if reco_dif > reco_dif_actual:
                    todosaqui = todosaqui + '<li><b>'+terminal_opcional['modelo'] + '</b>(' + str(reco_dif) + ') Añade: + ' + str(math.fabs(suma_rent)) + '€</li>'

            #si no se ha definido todos aquí es que no hay ningún equipo que mejore la rentabilidad de esta línea
            if not todosaqui:
                todosaqui = 'Lo sentimos. No encontramos recomendaciones!'

            if terminal == 'sin_terminal':
                todosaqui = 'Sin terminal, no existen recomendaciones.'




        #SI ES IEW VENTA A PLAZOS!!!
        #------------------------------------------------------------------------
        if grupo_tarifa=='iew' and vapsub=='si_vap':

            if cuota ==0:
                cuota_vap_float = 0
            elif cuota !='-':
                #cuanto paga el cliente en vap. total (pvp + cuotas24)
                cuota_vap_float = float(cuota.replace(',','.'))
                cliente_vap_pago_total = int(pvp) + cuota_vap_float*24 #cuáto paga el cliente por el terminal que se ha elegido?

            #obtener los intervalos de precio de cesión que busco
            i_inferior = precio - (precio*0.8)
            i_superior = 2000

            #obtener filtro con intervalos y de la misma gama
            reco_listado = OT_iew_vap.objects.filter(gama_jorge=gama_jorge ,precio__gte=i_inferior, precio__lte=i_superior).values()

            #por cada uno de los resultados obtener el dxc-precio
            reco_dif_actual = dxc-precio
            todosaqui= ''
            mgequipo = dxc-precio

            #Por cada uno de los terminales con precio mayor o 5% inferior:....
            for terminal_opcional in reco_listado:

                #Si es una línea con margen = 0, no hay mucho que mejorar, entonces buscar pago total cliente
                if mgequipo == 0 and terminal_opcional['cuota'+str(columna)]!='-': #(nunca va a haber en vap un dxc mayor que el precio de cesión)
                    pago_cliente_vap_reco = int(terminal_opcional['pago'+str(columna)])
                    cuota_cliente_vap_reco  = float(terminal_opcional['cuota'+str(columna)].replace(',','.'))*24
                    cliente_vap_pago_total_reco = pago_cliente_vap_reco + cuota_cliente_vap_reco

                    #si lo que paga el cliente en reco es menor que lo que paga con el equipo elegido...
                    if cliente_vap_pago_total_reco<cliente_vap_pago_total:
                        terminal_vap_reco_sobre_cliente = True
                        mg_pago_total_actual_reco = cliente_vap_pago_total - cliente_vap_pago_total_reco
                        todosaqui = todosaqui + '<li><b>'+terminal_opcional['modelo']+' (paga en total ' + str("%.2f" % mg_pago_total_actual_reco) + '€ menos)</li></b>'

                else: #si el margen de equipo es negativo....
                    #obtener el margen de equipo del terminal a recomendar
                    reco_dif = terminal_opcional['dxc'+str(columna)] - terminal_opcional['precio']

                    if linea_sin_dxc == False:
                        reco_dif = terminal_opcional['dxc'+str(columna)] - terminal_opcional['precio'] #con esto obtendo el mg del equipo. negativo si precio>dxc
                    else:
                        reco_dif = 0 - terminal_opcional['precio'] #con esto obtendo el mg del equipo. negativo si precio>dxc

                    #cuánto añadimos a la rentabilidad de la línea si elegimos este otro????
                    suma_rent   = math.fabs(mgequipo-reco_dif)

                    #obviamente: solo si: el margen de la recomendación es mayor al elegido.....
                    if reco_dif > reco_dif_actual:
                        todosaqui = todosaqui + '<li><b>'+terminal_opcional['modelo'] + '</b>(' + str(reco_dif) + ') Añade: + ' + str(math.fabs(suma_rent)) + '€</li>'

            #si no se ha definido todos aquí es que no hay ningún equipo que mejore la rentabilidad de esta línea
            if not todosaqui:
                todosaqui = 'Lo sentimos. No encontramos recomendaciones!'

            if terminal == 'sin_terminal':
                todosaqui = 'Sin terminal, no existen recomendaciones.'

        #FIN RECOMNDACIONES---------------------------------------

        #PRIMAS!! DEFINIR Y CÁLCULAS INFRAESTRUCTURAS (FUERA DE LOOP!)
        # ----------------------------------------------------------------
        # PRIMA DE VOLUMEN:




        #devolver datos!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        data = {}
        data['unidades'] = unidades
        data['dxc'] = dxc
        data['precio'] = precio
        data['voz'] = com_voz
        data['datos'] = com_datos
        data['extra'] = com_extra
        data['sva'] = com_sva
        data['modelo'] = terminal
        data['pvp'] = pvp
        data['cuota'] = cuota
        data['aviso'] = avisos
        data['rent'] = rent
        data['total'] = total
        data['todosaqui'] = todosaqui
        data['foto'] = nombre_foto
        data['gama_jorge'] = gama_jorge
        data['comision_conecta'] = comision_conecta
        data['terminal_vap_reco_sobre_cliente'] = terminal_vap_reco_sobre_cliente
        data['esclientevalor_volumen'] = esclientevalor
        data['escliente_oficinaPlus'] = esclienteOficinaPlus
        data['comision_base_operaciones'] = comision_base_operaciones
        data['comision_conecta_operaciones'] = comision_acelerador_convergencia
        data['comision_iew_operaciones'] = comision_acelerador_iew
        data['prima_volumen_movil'] = round(comision_volumen,2)
        data['prima_volumen_fijo'] = round(prima_volumen_fijo,2)
        data['grupo_usuario'] = grupo_usuario




        array_devuelto.append(data)



    json_string = json.dumps(array_devuelto)

    return HttpResponse(json_string, content_type='application/json')


#FUNCIÓN OBTENER INFORMACIÓN DEL MODELO. SWAL
#-------------------------------------------------------
@login_required
def ajax_obtener_info_modelo(request):
    terminal = request.GET.get('modelo')
    info_modelo = TerminalesMaestro.objects.values().filter(modelo=terminal)[0]['info_modelo']
    foto_nombre = TerminalesMaestro.objects.values().filter(modelo=terminal)[0]['nombre_foto']
    foto = TerminalesMaestro.objects.values().filter(modelo=terminal)[0]['foto_modelo']


    return HttpResponse(json.dumps({"info": info_modelo, 'foto_nombre':foto_nombre, 'foto':foto}),
            content_type="application/json")


#FUNCIÓN GUARDAR CONFIGURAUDOR EN BASE DE DATOS
#-------------------------------------------------------
@login_required
def guardarConfiguradorBD(request):


    datos = dict(request.GET) #tengo que convertirlo en un diccionario porque
    #me devuelve un QueryDict y me está resultando imposible acceder a algunos elementos

    #asignar variables principales (todo lo que devuelve es una lista, para acceder hay que añadir el [0])
    razon_social = datos['razon_social'][0]
    cif_nif = str(datos['cif_nif'][0])
    n_lineas_diferentes  = int(datos['filas'][0]) # esto es el numero de filas configuradas.
    total_lineas = int(datos['total_lineas'][0])
    username = request.user.username

    #primero tengo que hacer otro loop para ver algunas variables totales
    totalUpfront = 0
    for i in range(n_lineas_diferentes):
        totalUpfront = totalUpfront + int(datos['lineas_rentabilidad['+str(i)+'][total]'][0])


    for i in range(n_lineas_diferentes):
        print('--------fila ' + str(i) + '---------------')
        #datos sobre la línea ba´scos (datos configurados)
        nlineas = datos['lineas_configuradas['+str(i)+'][]'][0]
        tarifa = datos['lineas_configuradas['+str(i)+'][]'][1]
        origen = datos['lineas_configuradas['+str(i)+'][]'][2]
        paquete_datos = datos['lineas_configuradas['+str(i)+'][]'][3]
        cv = datos['lineas_configuradas['+str(i)+'][]'][4]
        mfo = datos['lineas_configuradas['+str(i)+'][]'][5]
        modelo_subvencion = datos['lineas_configuradas['+str(i)+'][]'][6]
        terminal = datos['lineas_configuradas['+str(i)+'][]'][7]

        #---------------datos de comisiones----------------------------------------------
        #datos sobre las comisiones calculadas
        comision_voz = datos['lineas_rentabilidad['+str(i)+'][voz]'][0]
        comision_datos = datos['lineas_rentabilidad['+str(i)+'][datos]'][0]
        comision_terminal = datos['lineas_rentabilidad['+str(i)+'][extra]'][0]
        comision_sva = datos['lineas_rentabilidad['+str(i)+'][sva]'][0]
        precio = datos['lineas_rentabilidad['+str(i)+'][precio]'][0]
        dxc = datos['lineas_rentabilidad['+str(i)+'][dxc]'][0]
        comision_fija = datos['lineas_rentabilidad['+str(i)+'][comision_conecta]'][0]

        #cuotas y pagos
        cuota = datos['lineas_rentabilidad['+str(i)+'][cuota]'][0]
        pvp = datos['lineas_rentabilidad['+str(i)+'][pvp]'][0]

        #rentabilidades
        rentabilidad_porLinea = totalUpfront/int(total_lineas)
        totalUpfront = totalUpfront

        #primas
        prima_opex_base =datos['lineas_rentabilidad['+str(i)+'][comision_base_operaciones]'][0]
        prima_opex_conecta = datos['lineas_rentabilidad['+str(i)+'][comision_conecta_operaciones]'][0]
        prima_opex_iew =datos['lineas_rentabilidad['+str(i)+'][comision_iew_operaciones]'][0]
        prima_opex_iew =datos['lineas_rentabilidad['+str(i)+'][comision_iew_operaciones]'][0]
        prima_volumen_movil =datos['lineas_rentabilidad['+str(i)+'][prima_volumen_movil]'][0]
        prima_volumen_fijo =datos['lineas_rentabilidad['+str(i)+'][prima_volumen_fijo]'][0]

        #otros datos
        foto = datos['lineas_rentabilidad['+str(i)+'][foto]'][0]


        escliente_oficinaPlus = datos['lineas_rentabilidad['+str(i)+'][escliente_oficinaPlus]'][0]
        esclientevalor_volumen = datos['lineas_rentabilidad['+str(i)+'][esclientevalor_volumen]'][0]

        #me da un error en los booleanos, no sé porque me parecen como true cuando debe ser True
        if escliente_oficinaPlus =='true':
            escliente_oficinaPlus = True
        else:
            escliente_oficinaPlus= False
        if esclientevalor_volumen =='true':
            esclientevalor_volumen= True
        else:
            esclientevalor_volumen= False


        gama_jorge = datos['lineas_rentabilidad['+str(i)+'][gama_jorge]'][0]
        aviso = datos['lineas_rentabilidad['+str(i)+'][aviso]'][0]

        #------------GUARDAR EN BASE DE DATOS----------------------------
        # ------------------------------------------------------------------
        p1 = OperacionesConfiGuardadas(
        #datos de operación
        razon_social = razon_social,
        cif_nif = cif_nif,
        n_lineas_diferentes = n_lineas_diferentes,
        total_lineas = total_lineas,

        #datos impuestos
        usuario = username,

        #datos linea configurada
        nlineas =nlineas,
        tarifa = tarifa,
        origen = origen,
        paquete_datos = paquete_datos,
        cv = cv,
        mfo = mfo,
        modelo_subvencion = modelo_subvencion,
        terminal = terminal,

        #datos comisiones princiaples
        comision_voz= comision_voz,
        comision_datos= comision_datos,
        comision_terminal= comision_terminal,
        comision_sva= comision_sva,
        precio= precio,
        dxc= dxc,
        comision_fija= comision_fija,

        #cuotas y pagos
        cuota= cuota,
        pvp= pvp,

        #rentabilidades
        rentabilidad_porLinea = rentabilidad_porLinea,
        totalUpfront = totalUpfront,

        #primas
        prima_opex_base =prima_opex_base,
        prima_opex_conecta = prima_opex_conecta,
        prima_opex_iew =prima_opex_iew,
        prima_volumen_movil =prima_volumen_movil,
        prima_volumen_fijo =prima_volumen_fijo,

        #otros datos
        foto = foto,
        escliente_oficinaPlus = escliente_oficinaPlus,
        esclientevalor_volumen = esclientevalor_volumen,
        gama_jorge = gama_jorge,
        aviso = aviso
        )
        p1.save()



    return HttpResponse(json.dumps({"resultado": 'guardado_correctamente'}),
            content_type="application/json")


    username = request.user.username
    # tabla = valores_unicos.filter(usuario=username)
    # tabla = OperacionesConfiGuardadas.objects.order_by('razon_social').values('razon_social').distinct()
    # tabla =  OperacionesConfiGuardadas.objects.all().filter(usuario=username)

#EXPORT CSV
def export_csv(request):

    username = request.user.username
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="asociados.csv"'

    writer = csv.writer(response)

    #SI ES UN COMERCIAL, MOSTRAR ESTAS COLUMNAS
    if (request.user.groups.filter(name='comercial').exists()):
        print('es comercial del grupo')
        writer.writerow([
            'razon_social', 'cif_nif', 'n_lineas_diferentes',
            'total_lineas', 'fecha', 'tarifa', 'origen', 'paquete_datos', 'cv',
            'mfo', 'modelo_subvencion','terminal','comision_voz','comision_datos',
            'comision_terminal','comision_sva','precio','dxc','comision_fija',
            'cuota','pvp','rentabilidad_porLinea','totalUpfront',
            'escliente_oficinaPlus','esclientevalor_volumen','aviso'])

        operaciones =OperacionesConfiGuardadas.objects.all().filter(usuario=username).values_list(
        'razon_social', 'cif_nif', 'n_lineas_diferentes',
        'total_lineas', 'fecha', 'tarifa', 'origen', 'paquete_datos', 'cv',
        'mfo', 'modelo_subvencion','terminal','comision_voz','comision_datos',
        'comision_terminal','comision_sva','precio','dxc','comision_fija',
        'cuota','pvp','rentabilidad_porLinea','totalUpfront',
        'escliente_oficinaPlus','esclientevalor_volumen','aviso')

    #SI no ES UN COMERCIAL, MOSTRAR ESTAS COLUMNAS
    else:
        print('no es comercial')
        writer.writerow([
            'razon_social', 'cif_nif', 'n_lineas_diferentes',
            'total_lineas', 'fecha', 'tarifa', 'origen', 'paquete_datos', 'cv',
            'mfo', 'modelo_subvencion','terminal','comision_voz','comision_datos',
            'comision_terminal','comision_sva','precio','dxc','comision_fija',
            'cuota','pvp','rentabilidad_porLinea','totalUpfront','prima_opex_base',
            'prima_opex_conecta','prima_opex_iew','prima_volumen_movil','prima_volumen_fijo',
            'escliente_oficinaPlus','esclientevalor_volumen','aviso'])

        operaciones =OperacionesConfiGuardadas.objects.all().filter(usuario=username).values_list(
        'razon_social', 'cif_nif', 'n_lineas_diferentes',
        'total_lineas', 'fecha', 'tarifa', 'origen', 'paquete_datos', 'cv',
        'mfo', 'modelo_subvencion','terminal','comision_voz','comision_datos',
        'comision_terminal','comision_sva','precio','dxc','comision_fija',
        'cuota','pvp','rentabilidad_porLinea','totalUpfront','prima_opex_base',
        'prima_opex_conecta','prima_opex_iew','prima_volumen_movil','prima_volumen_fijo',
        'escliente_oficinaPlus','esclientevalor_volumen','aviso')

    for a in operaciones:
        writer.writerow(a)

    return response


# **********************************************************************************
# EXPORT EXCEL xls
def export_xls(request):
    username = request.user.username
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Operaciones.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('operaciones')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    #SI ES COMERCIAL, HACER ESTO:
    if (request.user.groups.filter(name='comercial').exists()):
        print('es comercial')
        columns = [
            'razon_social', 'cif_nif', 'n_lineas_diferentes',
            'total_lineas', 'tarifa', 'origen', 'paquete_datos', 'cv',
            'mfo', 'modelo_subvencion','terminal','comision_voz','comision_datos',
            'comision_terminal','comision_sva','precio','dxc','comision_fija',
            'cuota','pvp','rentabilidad_porLinea','totalUpfront',
            'escliente_oficinaPlus','esclientevalor_volumen','aviso']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()

        rows = OperacionesConfiGuardadas.objects.all().filter(usuario=username).values_list(
        'razon_social', 'cif_nif', 'n_lineas_diferentes',
        'total_lineas', 'tarifa', 'origen', 'paquete_datos', 'cv',
        'mfo', 'modelo_subvencion','terminal','comision_voz','comision_datos',
        'comision_terminal','comision_sva','precio','dxc','comision_fija',
        'cuota','pvp','rentabilidad_porLinea','totalUpfront',
        'escliente_oficinaPlus','esclientevalor_volumen','aviso')

    #SI ES COMERCIAL, HACER ESTO:
    else:
        print('NO es comercial')
        columns = [
            'razon_social', 'cif_nif', 'n_lineas_diferentes',
            'total_lineas', 'tarifa', 'origen', 'paquete_datos', 'cv',
            'mfo', 'modelo_subvencion','terminal','comision_voz','comision_datos',
            'comision_terminal','comision_sva','precio','dxc','comision_fija',
            'cuota','pvp','rentabilidad_porLinea','totalUpfront','prima_opex_base',
            'prima_opex_conecta','prima_opex_iew','prima_volumen_movil','prima_volumen_fijo',
            'escliente_oficinaPlus','esclientevalor_volumen','aviso']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()

        rows = OperacionesConfiGuardadas.objects.all().filter(usuario=username).values_list(
        'razon_social', 'cif_nif', 'n_lineas_diferentes',
        'total_lineas', 'tarifa', 'origen', 'paquete_datos', 'cv',
        'mfo', 'modelo_subvencion','terminal','comision_voz','comision_datos',
        'comision_terminal','comision_sva','precio','dxc','comision_fija',
        'cuota','pvp','rentabilidad_porLinea','totalUpfront','prima_opex_base',
        'prima_opex_conecta','prima_opex_iew','prima_volumen_movil','prima_volumen_fijo',
        'escliente_oficinaPlus','esclientevalor_volumen','aviso')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response





#----------------------------------------------------------------------
#import export resources para el admin
#----------------------------------------------------------------------

from confi.resources import OTmultiHasta20Resource
@login_required
def export_admin_csv(request):
    modelo = OTmultiHasta20Resource()
    dataset = modelo.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="otMultiHasta20.csv"'
    return response
