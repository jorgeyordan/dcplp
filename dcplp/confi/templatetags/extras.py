
from django import template
from django.contrib.auth.models import User, Group

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False

    # se utiliza del siguiente modo en plantillas
    # {% load extras %} #donde extras el nombre del archivo py donde va el registro y la función
    # {% if request.user|has_group:"director_este" %}
    #
    # {% else %}


# Para utiilzarlo directamente en una vista:
# print(request.user.groups.filter(name='director').exists()) #devuelve true
#si el usuario está en el grupo de directores
