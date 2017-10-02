# coding=utf-8

import datetime
from django.db.models import Q
from incidencias.models import Incidencia
from incidencias.constantes import Constantes


class Buscador:
    # Definición del constuctor del buscador
    def __init__(
            self,
            catalogos,
            areas,
            items,
            rango_de_fecha_creacion_desde,
            rango_de_fecha_creacion_hasta,
    ):

        self.catalogos = catalogos
        self.areas = areas
        self.items = items

        # Parámetros con comportamiento de rango.
        self.rango_de_fecha_creacion_desde = rango_de_fecha_creacion_desde
        self.rango_de_fecha_creacion_hasta = rango_de_fecha_creacion_hasta

    def buscar(self):

        query = Q()

        if (self.catalogos is not None):
            query = query & Q(item__area__catalogo__id__in=self.catalogos)

        if (self.areas is not None):
            query = query & Q(item__area__id__in=self.alineaciones)

        if (self.items is not None):
            query = query & Q(item__id__in=self.temas)

        if self.rango_de_fecha_creacion_desde is not None:
            query_date = datetime.datetime.strptime(self.rango_de_fecha_creacion_desde, Constantes.FORMATO_FECHA).date()
            query = query & Q(fecha_creacion__gte=query_date)

        if self.rango_de_fecha_creacion_hasta is not None:
            query_date = datetime.datetime.strptime(self.rango_de_fecha_creacion_hasta, Constantes.FORMATO_FECHA).date()
            query = query & Q(fecha_creacion__lte=query_date)

        if query is not None:
            print(query)
            compromisos = Incidencia.objects.filter(query)
        else:
            print("Query is empty")
            compromisos = Incidencia.objects.all()

        return compromisos
