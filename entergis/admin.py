# -*- coding: utf-8 -*-
#   Author: Cristian Salamea - ovnicraft@gmail.com
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__author__ = 'Cristian Salamea (cristian.salamea@gntuhink.com)'

from django.conf import settings # needed we use the GOOGLE_MAPS_API_KEY
from models import * #Emprendimiento, Activity, Actor, TipoActor, Representante, Product, Ubicacion, Canton
from django.contrib import admin
from django.contrib.gis.admin import GeoModelAdmin
from django.contrib import databrowse

databrowse.site.register(Emprendimiento)

USE_GOOGLE_STREET_TILES = True

import pdb

class EnterGisAdmin(GeoModelAdmin):
    if USE_GOOGLE_STREET_TILES:
      map_template = 'gis/admin/google.html'
      extra_js = ['http://openstreetmap.org/openlayers/OpenStreetMap.js',
                  'http://maps.google.com/maps?file=api&amp;v=2&amp;key=%s' % settings.GOOGLE_MAPS_API_KEY]
    
    scrollable = False
    map_width = 700
    map_height = 325


class RepresentanteInLine(admin.StackedInline):
    model = Representante

class AreaGisAdmin(EnterGisAdmin):

    list_display = ['nombre', 'actividad']
    list_filter = ['actividad']

    fieldsets = [
        ('Informacion', {'fields': (('nombre', 'actividad', 'poly', 'productos')),
                         'classes': ('show', 'extrapretty')})
        ]

class EmprendimientoGisAdmin(EnterGisAdmin):

    list_display = ['nombre','representante', 'num_socios', 'num_acuerdo_min', 'url_info']
    
    search_fields = ('nombre','representante', 'num_socios',
                     'num_acuerdo_min', 'activity', 'area_produccion',
                     'area_procesamiento', 'parroquia', 'canton')
    
    list_filter = ['activity']
    list_per_page = 30
    
    fieldsets = (
      (u'Información', {'fields': (('nombre', 'representante', 'num_socios','url_info',
                                   'num_acuerdo_min', 'activity', 'phone')),
                       'classes': ('show','extrapretty', 'collapse')}),
      
      ('Productos', {'fields': (('productos',)),
                     'classes': ('wide',)}),

      (u'Producción', {'fields': (('area_produccion', 'area_procesamiento')),
                       'classes': ('show','extrapretty')}),

      (u'Ubicaciones', {'fields': (('ubicaciones',)),
                        'classes': ('wide',)}),

      (u'Ubicación Política', {'fields': (('parroquia', 'canton')),
                               'classes': ('wide',)}),

      ('Info Adicional', {'fields': (('info',)),
                          'classes': ('show','collapse-closed')}),
      
      ('Vista de Mapa Editable', {'fields': ('point',),
                                  'classes': ('show', 'wide')}),
    )    
    
class ActorAdmin(EnterGisAdmin):

    list_display = ['nombre', 'direccion', 'tipo']
    search_fields = ('nombre', 'direccion', 'tipo')
    ordering = ['tipo']
    list_filter = ['tipo']
    list_per_page = 30
    fieldsets = (
        ('Informacion de Entidades Publicas y Privadas', {'fields': ('nombre', 'direccion', 'tipo', 'tecnicos'),
                                                          'classes': ('show', 'extrapretty')}),
        ('Vista de Mapa Editable', {'fields': ('poly',),
                                    'classes': ('show', 'wide')})
        )


class RepresentanteAdmin(GeoModelAdmin):

    list_display = ['first_name', 'last_name', 'phone', 'gender', 'edad']
    search_fields = ('first_name', 'last_name', 'phone', 'gender', 'edad')
    ordering = ['first_name', 'last_name']
    list_filter = ['gender']
    fieldsets = (
        (u'Información', {'fields': ('first_name', 'last_name', 'phone', 'gender', 'edad'),
                          'classes': ('show', 'wide')}),
        )

class ActivityAdmin(GeoModelAdmin):
    
    list_display = ['code','name', 'uom', 'area', 'quantity_produced']
    search_fields = ['code','name', 'uom']
    list_filter = ['uom']
    
    fieldsets = (
        (u'Información', {'fields': ('code','name')}),
        ('Adicional', {'fields': ('uom', 'quantity_produced','area' ,'product'), 'classes': ('show','collapse-close')}),
        )

    
admin.site.register(Emprendimiento, EmprendimientoGisAdmin)
admin.site.register(Actor, ActorAdmin)
admin.site.register(Representante, RepresentanteAdmin)
admin.site.register(Product)
admin.site.register(Ubicacion)
#admin.site.register(Canton, CantonAdmin)
admin.site.register(ProductivityArea, AreaGisAdmin)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(TipoActor)


