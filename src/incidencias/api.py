# coding=utf-8

# Librerías extras de Django requeridas para la manipulación de la información.
from django.db.models import QuerySet
from django.views.generic.list import ListView
from django.http.response import HttpResponse
from django.db.models import Q
from django.db.models.aggregates import Sum, Count
from datetime import date, timedelta

# Imports provenientes del modelo de compromisos.
from incidencias.models import Catalogo, Area, Item

# Utilidades propias a utilizar dentro del API.
from sistemaIncidencias.utilities.utilities import Utilities
from incidencias.buscador import Buscador

'''
    Funciones definidas fuera de una estructura de clase, para ser consumida por las clases y otras funciones
    declaradas en este script.
'''


def get_array_or_none(the_string):
    '''
    Función que convierte un string de valores separados por coma, en una arreglo. En caso de que el string no
    esté definido o esté vacío, retorna None.
    :param the_string: variable a ser convertida.
    :return: arreglo con los valores del string o None.
    '''
    if the_string is None:
        return None
    else:
        return map(int, the_string.split(','))


'''
    Definición de los endpoints tipo REST.
'''


# endpoint para devolver determinado modelo en formato JSON. La url es /incidencias/api/"modelo"
class ModelosEndpoint(ListView):
    def get(self, request, modelo):
        return HttpResponse(Utilities.query_set_to_dumps(modelo.objects.all().order_by('nombre')),
                            'application/json')


# endpoint que regresa todas las areas dependiendo una categoria.
# La url es /incidencias/api/get-area-por-catalogo?catalogo_id=1
class AreasPorCategoriaEndpoint(ListView):
    def get(self, request, **kwargs):
        catalogo = request.GET.get('catalogo_id')
        areas = Area.objects.filter(catalogo=catalogo).order_by('nombre')
        respuesta = []
        for area in areas:
            registro = {
                "area_id": str(area.id),
                "area_nombre": area.nombre,
                "catalogo_id": str(area.catalogo.id),
                "catalogo_nombre": area.catalogo.nombre,
            }
            respuesta.append(registro)
        print(respuesta)
        return HttpResponse(Utilities.json_to_dumps(respuesta), 'application/json')


# Endpoint que regresa todos los items dependiente una area.
# URL incidencias/api/get-items-por-area?area_id=1
class ItemsPorAreaEndpoint(ListView):
    def get(self, request, **kwargs):
        area = request.GET.get('area_id')
        items = Item.objects.filter(area__id=area)
        return HttpResponse(Utilities.query_set_to_dumps(items), 'application/json')


class BuscadorIncidencias(ListView):
    def get(self, request, **kwargs):
        return  #