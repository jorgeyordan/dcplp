from django.db import models

# BASE DE DATOS PARA ALMACENAR DATOS DEL USUARIO AL HACER LOGIN
# ******************************************************************
class UserLoginActivity(models.Model):

    # Login Status
    login_IP = models.GenericIPAddressField(null=True, blank=True)
    login_datetime = models.DateTimeField(auto_now=True)
    login_username = models.CharField(max_length=40, null=True, blank=True)
    user_agent_info = models.CharField(max_length=255)
    esmovil = models.CharField(max_length=500, null=True, blank=True)

    #tipo acceso
    esmovil = models. NullBooleanField()# returns True)
    establet = models. NullBooleanField() # returns False
    estactil = models. NullBooleanField() # returns True
    espc = models. NullBooleanField() # returns False
    esbot = models. NullBooleanField() # returns False

    # Accessing user agent's browser attributes
    navegador =models.CharField(max_length=500, null=True, blank=True)
    familianav= models.CharField(max_length=500, null=True, blank=True)
    versionnav = models.CharField(max_length=500, null=True, blank=True)
    versionnav2 = models.CharField(max_length=500, null=True, blank=True)

    # Operating System properties
    os=models.CharField(max_length=500, null=True, blank=True)
    osfamilia = models.CharField(max_length=500, null=True, blank=True)
    osversion = models.CharField(max_length=500, null=True, blank=True)
    osversion2 = models.CharField(max_length=500, null=True, blank=True)

    # Device properties
    dispositivo=models.CharField(max_length=500, null=True, blank=True)
    dispositivofamilia = models.CharField(max_length=500, null=True, blank=True)

    #datos de localizació ip
    country = models.CharField(max_length=500, null=True, blank=True)
    city = models.CharField(max_length=500, null=True, blank=True)
    longi = models.CharField(max_length=500, null=True, blank=True)
    lat = models.CharField(max_length=500, null=True, blank=True)

    #login or user_logged user_logged_out
    login_logout = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return str(self.login_username)

    class Meta:
        verbose_name = 'user_login_activity'
        verbose_name_plural = 'user_login_activities'



# BASE DE DATOS TODOS LOS TERMINALES MAESTRO
# ******************************************************************

class TerminalesMaestro(models.Model):

    modelo = models.CharField(max_length=500, null=False, blank=False)
    nombre_foto= models.CharField(max_length=500, null=False, blank=False)
    # tipo_jorge = models.CharField(choices=TIPO_MODELO_JORGE)
    tipo_jorge = models.CharField(max_length=500, null=False, blank=False)
    foto_modelo = models.ImageField(upload_to = 'static/images/terminales_modelos/')
    info_modelo = models.TextField()

    def __str__(self):
        return str(self.modelo)





# BASE DE DATOS OFERTA TÁCTICA SUBVENCIONADO + 20 MULTILÍNEA
# ******************************************************************
class OT_multi_hasta20(models.Model):
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=500)
    precio = models.IntegerField(default=0)
    canon = models.FloatField(default=0)
    gama = models.CharField(max_length=20)

    capta1 = models.IntegerField()
    capta2 = models.IntegerField()
    capta3 = models.IntegerField()
    capta4 = models.IntegerField()
    capta5 = models.IntegerField()

    porta1 = models.IntegerField()
    porta2 = models.IntegerField()
    porta3 = models.IntegerField()
    porta4 = models.IntegerField()
    porta5 = models.IntegerField()

    #estas dos las incluyo yo como personales
    nombre_foto = models.CharField(max_length=100)
    gama_jorge = models.CharField(max_length=100)

    def __str__(self):
        return str(self.modelo)


class OT_multi_desde20(models.Model):
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=500)
    precio = models.IntegerField(default=0)
    canon = models.FloatField(default=0)
    gama = models.CharField(max_length=20)

    capta1 = models.IntegerField()
    capta2 = models.IntegerField()
    capta3 = models.IntegerField()
    capta4 = models.IntegerField()
    capta5 = models.IntegerField()

    porta1 = models.IntegerField()
    porta2 = models.IntegerField()
    porta3 = models.IntegerField()
    porta4 = models.IntegerField()
    porta5 = models.IntegerField()

    #estas dos las incluyo yo como personales
    nombre_foto = models.CharField(max_length=100)
    gama_jorge = models.CharField(max_length=100)

    def __str__(self):
        return str(self.modelo)

    class Meta:
        ordering = ['modelo']

class OT_multi_vap(models.Model):
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=500)
    precio = models.IntegerField(default=0)
    canon = models.FloatField(default=0)
    gama = models.CharField(max_length=20)

    pago_unico_capta = models.IntegerField()
    pago1 = models.CharField(max_length=4)
    cuota1 = models.CharField(max_length=4)
    pago2 = models.CharField(max_length=4)
    cuota2 = models.CharField(max_length=4)
    pago3 = models.CharField(max_length=4)
    cuota3 =models.CharField(max_length=4)
    pago4 = models.CharField(max_length=4)
    cuota4 =models.CharField(max_length=4)
    pago5 = models.CharField(max_length=4)
    cuota5 = models.CharField(max_length=4)

    dxc_pago_unico = models.IntegerField()
    dxc1 = models.IntegerField()
    dxc2 = models.IntegerField()
    dxc3 = models.IntegerField()
    dxc4 = models.IntegerField()
    dxc5 = models.IntegerField()

    #estas dos las incluyo yo como personales
    nombre_foto = models.CharField(max_length=100)
    gama_jorge = models.CharField(max_length=100)

    def __str__(self):
        return str(self.modelo)



class OT_iew_sub(models.Model):
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=500)
    precio = models.IntegerField(default=0)
    canon = models.FloatField(default=0)
    gama = models.CharField(max_length=20)

    precio1 = models.IntegerField()
    precio2 = models.IntegerField()
    precio3 = models.IntegerField()
    precio4 = models.IntegerField()

    dxc1 = models.IntegerField()
    dxc2 = models.IntegerField()
    dxc3 = models.IntegerField()
    dxc4 = models.IntegerField()


    #estas dos las incluyo yo como personales
    nombre_foto = models.CharField(max_length=100)
    gama_jorge = models.CharField(max_length=100)

    def __str__(self):
        return str(self.modelo)

class OT_iew_vap(models.Model):
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=500)
    precio = models.IntegerField(default=0)
    canon = models.FloatField(default=0)
    gama = models.CharField(max_length=20)
    meses_cuota = models.IntegerField(default=0)

    pago_unico_capta = models.IntegerField()
    pago1 = models.CharField(max_length=4)
    cuota1 = models.CharField(max_length=4)
    pago2 = models.CharField(max_length=4)
    cuota2 = models.CharField(max_length=4)
    pago3 = models.CharField(max_length=4)
    cuota3 =models.CharField(max_length=4)
    pago4 = models.CharField(max_length=4)
    cuota4 =models.CharField(max_length=4)

    dxc_pago_unico = models.IntegerField()
    dxc1 = models.IntegerField()
    dxc2 = models.IntegerField()
    dxc3 = models.IntegerField()
    dxc4 = models.IntegerField()


    #estas dos las incluyo yo como personales
    nombre_foto = models.CharField(max_length=100)
    gama_jorge = models.CharField(max_length=100)

    def __str__(self):
        return str(self.modelo)

class Comisiones_multilinea(models.Model):
    tarifa =models.CharField(max_length=100)
    capta = models.IntegerField()
    porta = models.IntegerField()
    terminal_movil_capta = models.IntegerField()
    terminal_movil_porta = models.IntegerField()

class Comisiones_datos(models.Model):
    tarifa = models.CharField(max_length=100)
    comision = models.IntegerField()
    def __str__(self):
        return str(self.tarifa)

class Comisiones_iew(models.Model):
    tarifa = models.CharField(max_length=100)
    com10= models.IntegerField()
    com1_9 = models.IntegerField()

class Comisiones_conecta(models.Model):
    conecta = models.CharField(max_length=100)
    comision = models.IntegerField()
    puntos = models.IntegerField()
    canales = models.IntegerField()
    valor_volumen = models.BooleanField(default=False)
    columna_prima_operaciones = models.CharField(max_length=50, default='acelerador_conecta_4')
    columna_prima_operaciones_oficina_plus = models.CharField(max_length=50, default='comision_operaciones_0')

    def __str__(self):
        return str(self.conecta)


class Comisiones_prima_operaciones(models.Model):
    tamaño_pago = models.IntegerField(default=0)
    base = models.FloatField(default=0)
    acelerador_conecta_1 = models.FloatField(default=0)
    acelerador_conecta_2 = models.FloatField(default=0)
    acelerador_conecta_3 = models.FloatField(default=0)
    acelerador_conecta_4 = models.FloatField(default=0)
    acelerador_oplus_propia = models.FloatField(default=0)
    acelerador_oplus_indirecta_1a = models.FloatField(default=0)
    acelerador_iew_pro_1 = models.FloatField(default=0)
    acelerador_iew_pro_2 = models.FloatField(default=0)
    acelerador_iew_pro_3 = models.FloatField(default=0)
    comision_operaciones_0 = models.FloatField(default=0)
    def __str__(self):
        return str(self.tamaño_pago)


class OperacionesConfiGuardadas(models.Model):
    #datos de operación
    razon_social = models.CharField(max_length=300)
    cif_nif = models.CharField(max_length=9)
    n_lineas_diferentes = models.IntegerField()
    total_lineas = models.IntegerField()

    #datos impuestos
    usuario = models.CharField(max_length=300)
    fecha = models.DateTimeField(auto_now_add=True)

    #datos linea configurada
    nlineas = models.IntegerField()
    tarifa = models.CharField(max_length=50)
    origen = models.CharField(max_length=50)
    paquete_datos = models.CharField(max_length=50)
    cv = models.CharField(max_length=10)
    mfo = models.CharField(max_length=10)
    modelo_subvencion = models.CharField(max_length=10)
    terminal = models.CharField(max_length=500)

    #datos comisiones princiaples
    comision_voz= models.FloatField(default=0)
    comision_datos= models.FloatField(default=0)
    comision_terminal= models.FloatField(default=0)
    comision_sva= models.FloatField(default=0)
    precio= models.FloatField(default=0)
    dxc= models.FloatField(default=0)
    comision_fija= models.FloatField(default=0)

    #cuotas y pagos
    cuota= models.CharField(max_length=10)
    pvp= models.CharField(max_length=10)

    #rentabilidades
    rentabilidad_porLinea = models.FloatField(default=0)
    totalUpfront = models.FloatField(default=0)

    #primas
    prima_opex_base =models.FloatField(default=0)
    prima_opex_conecta = models.FloatField(default=0)
    prima_opex_iew =models.FloatField(default=0)
    prima_volumen_movil =models.FloatField(default=0)
    prima_volumen_fijo =models.FloatField(default=0)

    #otros datos
    foto = models.CharField(max_length=300)
    escliente_oficinaPlus = models.BooleanField(default=0)
    esclientevalor_volumen = models.BooleanField(default=0)
    gama_jorge = models.CharField(max_length=100)
    aviso = models.CharField(max_length=800)

    def __str__(self):
        return str(self.razon_social)

    class Meta:
       ordering = ['-fecha']
