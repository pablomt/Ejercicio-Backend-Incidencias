from django.contrib import admin

from .models import Catalogo, Area, Item, Incidencia


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
    list_filter = ('catalogo',)


# Administrador para el modelo de Item
class ItemAdmin(admin.ModelAdmin):
    model = Item
    fields = ('nombre', 'area',)
    search_fields = ('nombre', 'area__nombre',)
    list_display = ('id', 'nombre', 'area',)
    ordering = ['id', 'nombre', 'area__nombre']
    list_filter = ('area__catalogo',)


# Administrador para el modelo de Item
class IncidenciaAdmin(admin.ModelAdmin):
    model = Incidencia
    fields = ('item', 'fecha_creacion',)
    list_display = ('id', 'item', 'get_area', 'get_catalogo', 'fecha_creacion', 'fecha_actualizacion')
    search_fields = ('item__nombre', 'item__area__nombre',)
    ordering = ['id', 'item__nombre', 'item__area__nombre']
    list_filter = ('item__area__catalogo',)
    list_display_links = ('id', 'item')

    def get_area(self, obj):
        return str(obj.item.area.nombre)

    get_area.short_description = 'Área'
    get_area.admin_order_field = 'item__area__nombre'

    def get_catalogo(self, obj):
        return str(obj.item.area.catalogo.nombre)

    get_catalogo.short_description = 'Catálogo'
    get_catalogo.admin_order_field = 'item__area__catalogo__item'


# Se dan de alta las vistas para administrador de los distintos modelos.
# Cuando se edita una vista de admin se debe poner el modelo seguido del admin que se meodifico
admin.site.register(Catalogo, CatalogoAdmin)
admin.site.register(Area, AreaAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Incidencia, IncidenciaAdmin)
