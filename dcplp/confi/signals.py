#se crea nuevo archivo py de signals(este) se define la señal de receiver
#luego en apps.py se sobreescribe la función ready no sé para qué más la verdad
# http://amgcomputing.blogspot.com.es/2014/10/django-user-login-logout-signals.html

from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.conf import settings
import logging
import socket
import pygeoip

from confi.models import UserLoginActivity

@receiver(user_logged_in)
def sig_user_logged_in(sender, user, request, **kwargs):
    logger = logging.getLogger(__name__)
    logger.info("user logged in: %s at %s" % (user, request.META['REMOTE_ADDR']))
    ip = request.META['REMOTE_ADDR']

    #esta es la parte de middleware adicional instalada para ver desde donde se conecta el usuario
    # ------------------------------------------------------------------------------------------------
    # requiere instalar en settings: << 'django_user_agents.middleware.UserAgentMiddleware', >>
    # en settings aplicaciones << 'django_user_agents', >>

    # Let's assume that the visitor uses an iPhone...
    esmovil = request.user_agent.is_mobile # returns True
    establet = request.user_agent.is_tablet # returns False
    estactil = request.user_agent.is_touch_capable # returns True
    espc = request.user_agent.is_pc # returns False
    esbot = request.user_agent.is_bot # returns False

    # Accessing user agent's browser attributes
    navegador = request.user_agent.browser  # returns Browser(family=u'Mobile Safari', version=(5, 1), version_string='5.1')
    familianav= request.user_agent.browser.family  # returns 'Mobile Safari'
    versionnav = request.user_agent.browser.version  # returns (5, 1)
    versionnav2 = request.user_agent.browser.version_string   # returns '5.1'

    # Operating System properties
    os=request.user_agent.os  # returns OperatingSystem(family=u'iOS', version=(5, 1), version_string='5.1')
    osfamilia = request.user_agent.os.family  # returns 'iOS'
    osversion = request.user_agent.os.version  # returns (5, 1)
    osversion2 = request.user_agent.os.version_string  # returns '5.1'

    # Device properties
    dispositivo=request.user_agent.device  # returns Device(family='iPhone')
    dispositivofamilia = request.user_agent.device.family  # returns 'iPhone'

    #geolocalizar por ip
    # ------------------------------------------------------------------------------------------------
    try:
        rawdata = pygeoip.GeoIP('../static/other/GeoLiteCity.dat')
        data = rawdata.record_by_name(ip)
        country = data['country_name']
        city = data['city']
        longi = data['longitude']
        lat = data['latitude']
        print ('[x] '+str(city)+',' +str(country))
        print ('[x] Latitude: '+str(lat)+ ', Longitude: '+ str(longi))
    except:
        country = city = longi = lat = 'desconocido'

    #guardar en base de datos
    # ------------------------------------------------------------------------------------------------
    p1 = UserLoginActivity(login_IP= ip, login_username=user, user_agent_info=navegador,
     esmovil=esmovil, establet=establet, estactil=estactil, espc=espc, esbot=esbot,
     navegador=navegador, familianav=familianav, versionnav=versionnav, versionnav2=versionnav2,
     os=os, osfamilia=osfamilia, osversion=osversion, osversion2=osversion2, dispositivo=dispositivo, dispositivofamilia=dispositivofamilia,
     country=country, city=city, longi=longi, lat=lat, login_logout='login')
    p1.save()



@receiver(user_logged_out)
def sig_user_logged_out(sender, user, request, **kwargs):
    logger = logging.getLogger(__name__)
    p2 = UserLoginActivity(login_IP= request.META['REMOTE_ADDR'], login_username=user, login_logout='logout')
    p2.save()
