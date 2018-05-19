from .import views
from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required



urlpatterns = [
    path('', views.index, name='index'),
    path('login', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('terminales', views.terminales_ranking, name='terminales'),
    path('confi_multilinea', views.confi_multilinea, name='confi_multilinea'),
    path('configurador_ajax', views.configurador_ajax_view, name='configurador_ajax'),
    path('obtener_info_equipo_ajax', views.ajax_obtener_info_modelo, name='obtener_info_equipo_ajax'),
    path('guardarConfiBD', views.guardarConfiguradorBD, name='guardarConfiBD'),
    # path('operacion/<int:pk>/', login_required(views.OperacionesView.as_view()), name='detalle_operacion'),
    path('exportar_csv', views.export_csv, name='exportar_csv'),
    path('exportar_xls', views.export_xls, name='exportar_xls'),

]
