from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import (Comisiones_multilinea, OT_multi_hasta20, Comisiones_iew, Comisiones_datos, TerminalesMaestro,
Comisiones_prima_operaciones,Comisiones_conecta,OperacionesConfiGuardadas,UserLoginActivity,OT_multi_desde20,
OT_multi_vap,OT_iew_sub,OT_iew_vap)


##teoricamente se pone una clase y luego se registra. sin eeiquetas @ lo que estás viendo es la forma de trabajo de import export

# class ComisionDatosAdmin(admin.ModelAdmin):
#     list_display = ('tarifa', 'comision')
# admin.site.register(Comisiones_datos, ComisionDatosAdmin)


#para import export admin
@admin.register(UserLoginActivity)
class UserLoginActivityAdmin(ImportExportModelAdmin):
    list_display = ('login_username', 'login_IP','login_datetime', 'login_logout', 'country','city')
    list_filter = ('login_username', ) #crea un sidebar para filtro rapido. la verdad que es la polla
    ordering = ('login_datetime', ) #-'modelo'para ordenar de z a a  #ordnea los resultados
    search_fields = ('login_username', ) #crea un text box para buscar por el campo elegido

@admin.register(TerminalesMaestro)
class TerminalesMaestroAdmin(ImportExportModelAdmin):
    list_display = ('modelo', 'nombre_foto', 'tipo_jorge')
    list_filter = ('tipo_jorge', ) #crea un sidebar para filtro rapido. la verdad que es la polla
    ordering = ('modelo', ) #-'modelo'para ordenar de z a a  #ordnea los resultados
    search_fields = ('modelo', ) #crea un text box para buscar por el campo elegido

@admin.register(OT_multi_hasta20)
class OTmultihasta20Admin(ImportExportModelAdmin):
    list_display = ('modelo', 'precio', 'marca')
    list_filter = ('marca',) #crea un sidebar para filtro rapido. la verdad que es la polla
    ordering = ('modelo', ) #-'modelo'para ordenar de z a a  #ordnea los resultados
    search_fields = ('modelo', ) #crea un text box para buscar por el campo elegido

@admin.register(OT_multi_desde20)
class OT_multi_desde20Admin(ImportExportModelAdmin):
    list_display = ('marca', 'modelo', 'precio')
    list_filter = ('marca',) #crea un sidebar para filtro rapido. la verdad que es la polla
    ordering = ('modelo',) #-'modelo'para ordenar de z a a  #ordnea los resultados
    search_fields = ('modelo',) #crea un text box para buscar por el campo elegido

@admin.register(OT_multi_vap)
class OT_multi_vapAdmin(ImportExportModelAdmin):
    list_display = ('marca', 'modelo', 'precio')
    list_filter = ('marca',) #crea un sidebar para filtro rapido. la verdad que es la polla
    ordering = ('modelo',) #-'modelo'para ordenar de z a a  #ordnea los resultados
    search_fields = ('modelo',) #crea un text box para buscar por el campo elegido

@admin.register(OT_iew_sub)
class OT_iew_subAdmin(ImportExportModelAdmin):
    list_display = ('marca', 'modelo', 'precio')
    list_filter = ('marca',) #crea un sidebar para filtro rapido. la verdad que es la polla
    ordering = ('modelo',) #-'modelo'para ordenar de z a a  #ordnea los resultados
    search_fields = ('modelo',) #crea un text box para buscar por el campo elegido

@admin.register(OT_iew_vap)
class OT_iew_vapAdmin(ImportExportModelAdmin):
    list_display = ('marca', 'modelo', 'precio')
    list_filter = ('marca',) #crea un sidebar para filtro rapido. la verdad que es la polla
    ordering = ('modelo',) #-'modelo'para ordenar de z a a  #ordnea los resultados
    search_fields = ('modelo',) #crea un text box para buscar por el campo elegido


@admin.register(Comisiones_multilinea)
class Comisiones_multilineaAdmin(ImportExportModelAdmin):
    list_display = ('tarifa', 'capta', 'porta')

@admin.register(Comisiones_datos)
class Comisiones_datosAdmin(ImportExportModelAdmin):
     list_display = ('tarifa', 'comision')

@admin.register(Comisiones_iew)
class Comisiones_iewAdmin(ImportExportModelAdmin):
     list_display = ('tarifa', 'com1_9','com10')

@admin.register(Comisiones_conecta)
class Comisiones_conectaAdmin(ImportExportModelAdmin):
    list_display = ('conecta', 'comision', 'puntos', 'canales','valor_volumen','columna_prima_operaciones', 'columna_prima_operaciones_oficina_plus')
    list_filter = ('valor_volumen', ) #crea un sidebar para filtro rapido. la verdad que es la polla
    ordering = ('conecta', ) #-'modelo'para ordenar de z a a  #ordnea los resultados
    search_fields = ('conecta', ) #crea un text box para buscar por el campo elegido

@admin.register(Comisiones_prima_operaciones)
class Comisiones_prima_operacionesAdmin(ImportExportModelAdmin):
    list_display = ('tamaño_pago','base')


@admin.register(OperacionesConfiGuardadas)
class OperacionesConfiGuardadasAdmin(ImportExportModelAdmin):
    list_display = ('razon_social', 'usuario','fecha', 'n_lineas_diferentes', 'total_lineas','nlineas','origen', 'paquete_datos','rentabilidad_porLinea','totalUpfront')
    list_filter = ('usuario', ) #crea un sidebar para filtro rapido. la verdad que es la polla
    ordering = ('razon_social', ) #-'modelo'para ordenar de z a a  #ordnea los resultados
    search_fields = ('razon_social', ) #crea un text box para buscar por el campo elegido





# Register your models here.
# admin.site.register(OT_multi_hasta20)
