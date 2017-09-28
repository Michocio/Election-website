# W pliku definuje własne tagi, które mogę
# wykorzystać w templates do uzyskania danych dla
# poszczególnych informacji trzymanych w bazie danych

from django import template


register = template.Library()


@register.simple_tag
def get_procent(a, b):
    return round((a/b)*100,2)

@register.simple_tag
def dzielenie(a, b):
    return round((a/b),0)

@register.simple_tag
def get_wazne(dict, value):
    return dict[value].wazne

@register.simple_tag()
def get_kand_1(dict, value):
    return dict[value].kandydat_1

@register.simple_tag()
def get_kand_2(dict, value):
    return dict[value].kandydat_2

@register.simple_tag()
def get_procent_1(dict, value):
    return round((dict[value].kandydat_1 / max(1,dict[value].wazne)) * 100,2)

@register.simple_tag()
def get_procent_2(dict, value):
    return round(((dict[value].kandydat_2) / max(1,dict[value].wazne)) * 100,2)
