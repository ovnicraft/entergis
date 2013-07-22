from django.shortcuts import render_to_response
from models import *
from django.template import RequestContext
from django.contrib.gis.geos import MultiPoint
from django.conf import settings
from django.http import HttpResponse
from django.utils import simplejson
from django.core.serializers import serialize
from vectorformats.Formats import Django, GeoJSON, GeoRSS
from decimal import Decimal

import pdb

key2 = 'ABQIAAAAZJAxdUVOaDDgn3nLQQYuyRRc5N-P1NpY03Egq3jSesNMkYFHpRQfMd4FdScWYQkeGqFVGlXCvirASg'
#google_api = 'http://maps.google.com/maps/output=json&oe=utf8&sensor=true&key=ABQIAAAAZJAxdUVOaDDgn3nLQQYuyRQ7ewXWfe-qAGN7fhHFFe0sU51e7hS-SKZfZ7ktS40xR0GJa2kxqtcEbQ'
google_api = 'http://maps.google.com/maps?file=api&amp;v=2&amp;key=%s' % key2 #settings.GOOGLE_MAPS_API_KEY

__author__ = 'Cristian Salamea (cristian.salamea@gnuthink.com)'

def update_fields():
    for emp in Emprendimiento.objects.all():
        emp.m2m_tojson()
        emp.save()
        
    for zona in ProductivityArea.objects.all():
        zona.m2m_tojson()
        zona.save()

    for actor in Actor.objects.all():
        actor.m2m_tojson()
        actor.save()

def emprendimientos_by_activity(activities):
    prop_json = ['nombre','activity', 'url_info','num_socios', 'area_produccion', 'tipomodel', 'productos_json', 'ubicaciones_json','parroquia']
    childrens = []
    for act in activities:
        emps = Emprendimiento.objects.filter(activity=act)
        if emps:
            djf = Django.Django(geodjango='point', properties=prop_json)
            geoj = GeoJSON.GeoJSON()
            data_decoded = djf.decode(emps)
            string = geoj.encode(data_decoded)
            dict_act = {'leaf': True, 'id': 'M', 'cls': 'file'}
            dict_act['text'] = act.name
            dict_act['id'] = act.code
            dict_act['data'] = string
            dict_act['emprendimiento'] = True
            childrens.append(dict_act)
    return childrens

def emprendimientos_by_parroquia(parroquias):
    prop_json = ['nombre','activity', 'url_info','num_socios', 'area_produccion', 'tipomodel', 'productos_json', 'ubicaciones_json', 'parroquia']
    ch = []
    for par in parroquias:
        emps = Emprendimiento.objects.filter(parroquia=par)
        if emps:
            djf = Django.Django(geodjango='point', properties=prop_json)
            geoj = GeoJSON.GeoJSON()
            string = geoj.encode(djf.decode(emps))
            dict_par = {'leaf': True, 'id': 'parroquias', 'cls': 'file'}
            dict_par['text'] = par.dpa_despar
            dict_par['id'] = par.dpa_parroq
            dict_par['data'] = string
            dict_par['emprendimiento'] = True
            ch.append(dict_par)
    return ch

def prod_by_activity(activities):
    ch1 = []
    for act in activities:
        actprod = ProductivityArea.objects.filter(actividad=act)
        if actprod:
            djf = Django.Django(geodjango='poly', properties=['nombre', 'actividad', 'tipomodel', 'productos_json', 'parroquias_json'])
            geoj = GeoJSON.GeoJSON()
            data_decoded = djf.decode(actprod)
            string = geoj.encode(data_decoded)
            dict1 = {'leaf': True, 'id': 'productivas', 'cls': 'file'}
            dict1['text'] = act.name
            dict1['id'] = act.code
            dict1['data'] = string
            dict1['zona'] = True
            ch1.append(dict1)
    return ch1

def prod_by_parroquia(parroquias):
    ch = []
    for par in parroquias:
        actprods = ProductivityArea.objects.filter(parroquias=par)
        if actprods:
            djf = Django.Django(geodjango='poly', properties=['nombre', 'actividad', 'tipomodel', 'productos_json', 'parroquias_json'])
            geoj = GeoJSON.GeoJSON()
            data_decoded = djf.decode(actprods)
            string = geoj.encode(data_decoded)
            dict1 = {'leaf': True, 'id':'prod_par', 'cls': 'file'}
            dict1['text'] = par.des_par
            dict1['id'] = par.dpa_parroq
            dict1['data'] = string
            dict1['zona'] = True
            ch.append(dict1)
    return ch

def actores_by_tipo(tipos):
    ch = []
    for tipo in tipos:
        portipo = Actor.objects.filter(tipo=tipo)
        if portipo:
            djf = Django.Django(geodjango='poly', properties=['nombre', 'tipo', 'url_info','tecnicos_json', 'direccion', 'tipomodel'])
            geoj = GeoJSON.GeoJSON()
            data_decoded = djf.decode(portipo)
            string = geoj.encode(data_decoded)
            dict1 = {'leaf': True, 'id': 'actores_tipo', 'cls':'file'}
            dict1['text'] = tipo.nombre
            dict1['id'] =  tipo.codigo
            dict1['data'] = string
            ch.append(dict1)
    return ch

def emprendimientos(request):
    if request.method == u'POST':
        json_data = {}
        activities = Activity.objects.all()
        parroquias = Parroquia.objects.all()
        tipos = TipoActor.objects.all()
        childrens = emprendimientos_by_activity(activities)
        print "1"
        ch = emprendimientos_by_parroquia(parroquias)
        print "2"
        ch1 = prod_by_activity(activities)
        print 3
        ch2 = prod_by_parroquia(parroquias)
        chactores = actores_by_tipo(tipos)
        data = [{'text': 'Emprendimientos', 'id': 'companies', 'cls': 'folder',
                 'children': [{'text': 'Actividad Productiva', 'id': 'activity', 'cls': 'folder', 'children': childrens},
                              {'text': 'Por Parroquia', 'id': 'parroquia', 'cls': 'folder', 'children': ch}]
                 },{'text': 'Potencialidades Productivas', 'id': 'zonasproductivas', 'cls': 'folder',
                    'children': [{'text': 'Actividad Productiva', 'id': 'byactivdad', 'cls': 'folder', 'children': ch1},
                                 {'text': 'Por Parroquia', 'id': 'porparroquia', 'cls':'folder','children':ch2}]
                    },{'text': 'Actores', 'id': 'actores', 'cls': 'folder',
                       'children':[{'text': 'Tipos', 'id': 'bytipo', 'cls': 'folder', 'children': chactores}]
            }]
        json_data = simplejson.dumps(data)
    return HttpResponse(json_data, mimetype='application/json')

def search(request):
    if request.method == u'POST':
        regexp = POST.get('query')
        json_data = {}
        if regexp != "":
            count = query.count()
            data = [{'nombre': obj.nombre} for obj in query]
            json_data = json.dumps({'results':count, 'data': data})
            return HttpResponse(json_data, mimetype='application/json')
    else:
        GET = request.GET
        if GET.has_key('query') and GET.has_key('byid'):
            point_id = GET.get('query')
            emp = Emprendimiento.objects.filter(id=point_id).values(Empredimiento.fields_popup)
            json_data = simplejson.dumps(emp)
            return HttpResponse(json_data, mimetype='application/json')            
        

def homepage(request):
    update_fields()
    objects = Emprendimiento.objects.all()
    cantones = Canton.objects.all()
    actores = Actor.objects.all()
    areas = ProductivityArea.objects.all()
    p = []
    context = {
               'google_api': google_api,
               'object_list': objects,
               'cantones': cantones,
               'actores': actores,
               'areas': areas
               }    
    return render_to_response('home.html', context,
                              context_instance=RequestContext(request))

    


