# coding=utf-8

# Librerías extras de Django requeridas para la manipulación de la información.
from django.db.models import QuerySet
from django.views.generic.list import ListView
from django.http.response import HttpResponse
from django.db.models import Q
from django.db.models.aggregates import Sum, Count
from datetime import date, timedelta

# Este import se utilizara en la api para forzar al usuario a estar logeado para consumir las apis.
from django.contrib.auth.mixins import LoginRequiredMixin

# Imports provenientes del modelo de compromisos.
from incidencias.models import Catalogo, Area, Item, Incidencia

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
        return list(map(int, the_string.split(',')))


def get_incidencias_por_catalogo_area(incidencias_set=None, areas_array=None):
    '''
        Obtiene reporte para un posible dashboard general basado en las incidencias, contiene la siguiente estrucutura:
        incidencias_por_catalogo_area [{id_catalogo, nombre_catalogo, tema, num_insidencias [{id_area, nombre_area,
        num_area,}]}]
    '''
    reporte = []
    catalogo_set = Catalogo.objects.filter(id=2).order_by('id')

    if areas_array is None:
        areas_set = Area.objects.all().order_by('id')
    else:
        areas_set = Area.objects.filter(Q(id__in=areas_array))

    for catalogo in catalogo_set:
        registro = {
            "id_catalogo": catalogo.id,
            "nombre_catalogo": catalogo.nombre,
            "areas": [],
            "num_insidencias_por_catalogo": 0
        }
        for area in areas_set:
            if incidencias_set is None:
                incidencias_filtradas = Incidencia.objects.filter(Q(item__area__catalogo__id=catalogo.id),
                                                                  Q(item__area__id=area.id))
            else:
                incidencias_filtradas = incidencias_set.filter(Q(item__area__catalogo__id=catalogo.id),
                                                               Q(item__area__id=area.id))

            incidencias_set_areas = incidencias_filtradas.values('item__area__catalogo__id',
                                                                 'item__area__catalogo__nombre',
                                                                 'item__area__id').annotate(
                num_incidencias=Count('item__area'))
            registro_area = {
                "id_area": area.id,
                "nombre_area": area.nombre,
                "num_incidencias": 0,
            }

            for incidencias in incidencias_set_areas:
                registro_area['num_incidencias'] = incidencias['num_incidencias']
                registro["num_insidencias_por_catalogo"] = registro["num_insidencias_por_catalogo"] + incidencias[
                    'num_incidencias']
            registro['areas'].append(registro_area)
        reporte.append(registro)
        print(reporte)
    return reporte


'''
    Definición de los endpoints tipo REST.
'''


# endpoint para devolver determinado modelo en formato JSON. La url es /incidencias/api/"modelo"
class ModelosEndpoint(LoginRequiredMixin, ListView):
    def get(self, request, modelo):
        return HttpResponse(Utilities.query_set_to_dumps(modelo.objects.all().order_by('nombre')),
                            'application/json')


# endpoint que regresa todas las areas dependiendo una categoria.
# La url es /incidencias/api/get-areas-por-catalogo?catalogo_id=1
class AreasPorCategoriaEndpoint(LoginRequiredMixin, ListView):
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
class ItemsPorAreaEndpoint(LoginRequiredMixin, ListView):
    def get(self, request, **kwargs):
        area = request.GET.get('area_id')
        items = Item.objects.filter(area__id=area)
        return HttpResponse(Utilities.query_set_to_dumps(items), 'application/json')


class BuscadorIncidencias(LoginRequiredMixin, ListView):
    def get(self, request, **kwargs):
        response = {}
        buscador = Buscador(
            catalogos=get_array_or_none(request.GET.get('catalogos')),
            areas=get_array_or_none(request.GET.get('areas')),
            items=get_array_or_none(request.GET.get('items')),

            # Parámetros con comportamiento de rangos.
            rango_de_fecha_creacion_desde=request.GET.get('rango_de_fecha_creacion_desde'),
            rango_de_fecha_creacion_hasta=request.GET.get('rango_de_fecha_creacion_hasta'),
        )
        incidencias = buscador.buscar()

        # Reporte 1: obtener incidencias por area
        # Obtiene las incidencias agrupados por catalogo y por areas.
        response["indicencias_por_area"] = get_incidencias_por_catalogo_area(incidencias, get_array_or_none(
            request.GET.get('areas')))

        return HttpResponse(Utilities.json_to_dumps(response), 'application/json; charset=utf-8')
