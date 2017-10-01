from django.contrib import admin

from .models import Catalogo, Area, Item


# Register your models here.


# Administrador para el modelo de Catalogo
class CatalogoAdmin(admin.ModelAdmin):
    model = Catalogo
    fields = ('nombre',)
    search_fields = ('nombre',)
    list_display = ('id', 'nombre',)
    ordering = ['id', 'nombre', ]


# Administrador para el modelo de Área
class AreaAdmin(admin.ModelAdmin):
    model = Area
    fields = ('nombre', 'catalogo',)
    search_fields = ('nombre', 'catalogo__nombre',)
    list_display = ('id', 'nombre', 'catalogo',)
    ordering = ['id', 'nombre', 'catalogo__nombre']


# Administrador para el modelo de Item
class ItemAdmin(admin.ModelAdmin):
    model = Item
    fields = ('nombre', 'area',)
    search_fields = ('nombre', 'area__nombre',)
    list_display = ('id', 'nombre', 'area',)
    ordering = ['id', 'nombre', 'area__nombre']
    


# Se dan de alta las vistas para administrador de los distintos modelos.
# Cuando se edita una vista de admin se debe poner el modelo seguido del admin que se meodifico
admin.site.register(Catalogo, CatalogoAdmin)
admin.site.register(Area, AreaAdmin)
admin.site.register(Item, ItemAdmin)
