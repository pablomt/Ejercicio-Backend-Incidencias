# coding=utf-8
from django.db import models
from django.forms.models import model_to_dict


# Create your models here.

# *********************************************************************
#           Catalogo : Modelo para clasificar las areas
# *********************************************************************

class Catalogo(models.Model):
    # la pk(id) se crea por default
    # El campo nombre no puede ser null. El campo nombre es unico
    nombre = models.CharField(verbose_name="Nombre", max_length=100, db_index=True, unique=True)

    class Meta:
        verbose_name = "Catálogo"
        verbose_name_plural = "Catálogos"

    def __str__(self):
        return self.nombre

    def __unicode__(self):  # For Python 2
        return self.nombre

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['id'] = str(self.id)
        ans['nombre'] = self.nombre
        return ans


# *********************************************************************
#           Área : Modelo para clasificiar los items
# *********************************************************************

class Area(models.Model):
    # la pk(id) se crea por default
    # El campo nombre y catalogo no pueden ser null, El campo nombre es unico
    nombre = models.CharField(verbose_name="Área", max_length=100, db_index=True, )
    catalogo = models.ForeignKey(Catalogo, verbose_name="Catalogo")

    class Meta:
        verbose_name = "Área"
        verbose_name_plural = "Áreas"
        unique_together = ("nombre", "catalogo")

    def __str__(self):
        return self.nombre

    def __unicode__(self):  # For Python 2
        return self.nombre

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['id'] = str(self.id)
        ans['nombre'] = self.nombre
        return ans


# *********************************************************************
#           Item : Modelo para los items
# *********************************************************************

class Item(models.Model):
    # la pk(id) se crea por default
    # El campo nombre y catalogo no pueden ser null, El campo nombre es unico
    nombre = models.CharField(verbose_name="Item", max_length=100, db_index=True)
    area = models.ForeignKey(Area, verbose_name="Área")

    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"
        unique_together = ("nombre", "area")

    def __str__(self):
        return self.nombre

    def __unicode__(self):  # For Python 2
        return self.nombre

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['id'] = str(self.id)
        ans['nombre'] = self.nombre
        return ans


# *********************************************************************
#           Incidencia : Modelo para todas las incidencias
# *********************************************************************

class Incidencia(models.Model):
    # la pk(id) se crea por default
    # Se agregan dos nuevos campos a los requisitos: fecha_actualizacion y facha de cracion para futuros usos
    item = models.ForeignKey(Item, verbose_name="Item")
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Incidencia"
        verbose_name_plural = "Incidencias"

    def __str__(self):
        return self.nombre

    def __unicode__(self):  # For Python 2
        return self.nombre

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['id'] = str(self.id)
        ans['nombre'] = self.nombre
        return ans
