from django.conf.urls import url, include
from incidencias import api
from incidencias.api import ModelosEndpoint
from incidencias.models import Catalogo, Area, Item

urlpatterns = [
    url(r'^api/catalogo/$', ModelosEndpoint.as_view(), {'modelo': Catalogo}),
    url(r'^api/area/$', ModelosEndpoint.as_view(), {'modelo': Area}),
    url(r'^api/item/$', ModelosEndpoint.as_view(), {'modelo': Item}),
    url(r'^api/get-area-por-catalogo', api.AreasPorCategoriaEndpoint.as_view()),
    url(r'^api/get-items-por-area', api.ItemsPorAreaEndpoint.as_view()),
    url(r'^api/buscador-incidencias', api.BuscadorIncidencias.as_view()),


]