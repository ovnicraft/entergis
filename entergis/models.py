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

from django.contrib.gis.db import models
from vectorformats import Feature

class MaleManager(models.Manager):
    def get_query_set(self):
        return super(MaleManager,self).get_query_set().filter(gender='M')


class FemaleManager(models.Manager):
    def get_query_set(self):
        return super(FemaleManager,self).get_query_set().filter(gender='F')


class Representante(models.Model):
    GENDER_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    )
    first_name = models.CharField('Nombre', max_length=50)
    last_name = models.CharField('Apellido', max_length=50)
    phone = models.CharField('Telefono', max_length=50, blank=True)
    gender = models.CharField('Genero de Representante', max_length=1, choices=GENDER_CHOICES)
    edad = models.IntegerField('Edad', blank=True)

    class Meta:
        verbose_name = 'Representante'
        verbose_name_plural = 'Representantes'

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)


#class PAManager(models.Manager):
#    res = {}
#    def to_json(self):
#        for 

class Product(models.Model):
    name = models.CharField( max_length=50, verbose_name='Nombre')
    code = models.CharField(max_length=20, verbose_name= u'Código', blank=True)
    precio = models.DecimalField('Precio', max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return '%s' % self.name

    def to_json(self):
        return 'Producto 1, Producto 2'

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'


#tipos de emprendimientos
class Activity(models.Model):
    UoM = (
        ('m', 'METROS'),
        ('kg', 'KGs'),
        ('litro','LITROS'),
    )
    
    code = models.CharField(u'Código', max_length=20)
    name = models.CharField('Nombre', max_length=100)
    uom = models.CharField(max_length=10, choices=UoM, verbose_name='Unidad de Medida', blank=True)
    quantity_produced = models.IntegerField(verbose_name='Cant. Producida', blank=True, null=True, default=0)
    area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Area en Metros', blank=True, null=True, default=0.00)
    product = models.ForeignKey(Product, blank=True, null=True, verbose_name='Producto')

    def __str__(self):
        return '%s-%s' % (self.code, self.name)

    def __unicode__(self):
        return 'Emprendimiento de %s' % self.name

    def to_json(self):
        return '%s' % self.name

    class Meta:
        verbose_name = 'Actividad'
        verbose_name_plural = 'Tipo de Actividad'
        

class Ubicacion(models.Model):
    nombre = models.CharField('Nombre', max_length=100)

    def __str__(self):
        return '%s' % self.nombre

    class Meta:
        verbose_name = u'Ubicación'
        verbose_name_plural = 'Ubicaciones'


class Canton(models.Model):
    mapping = {
        'dpa_descan': 'DPA_DESCAN',
        'dpa_valor': 'DPA_VALOR',
        'dpa_canton': 'DPA_CANTON',
        'dpa_provin': 'DPA_PROVIN',
        'dpa_despro': 'DPA_DESPRO',
        'area': 'AREA',
        'mpoly':'POLYGON'
        }
    
    dpa_descan = models.CharField('Nombre', max_length=40)
    dpa_valor = models.IntegerField('VALOR')
    dpa_canton = models.CharField('Canton', max_length=20)
    dpa_provin = models.CharField('Provincia', max_length=20)
    dpa_despro = models.CharField('DESPRO', max_length=40)
    area = models.DecimalField('Area', max_digits=16, decimal_places=2)
    mpoly = models.MultiPolygonField('Mapa Cantonal')
    objects = models.GeoManager()

    class Meta:
        verbose_name = ('Canton')
        verbose_name_plural = ('Cantones del Azuay')

    def __unicode__(self):
        return u'Canton: %s - %s' % (self.dpa_descan, self.dpa_canton)

    def __str__(self):
        return '%s - %s' % (self.dpa_descan, self.dpa_canton)


class Parroquia(models.Model):
    mapping = {
        'dpa_parroq': 'DPA_PARROQ',
        'dpa_despar': 'DPA_DESPAR',
        'dpa_canton': 'DPA_CANTON',
        'dpa_provin': 'DPA_PROVIN',
        'dpa_despro': 'DPA_DESPRO',
        'dpa_descan': 'DPA_DESCAN',
        'mpoly':'POLYGON',
        }
    
    dpa_parroq = models.CharField('Codigo de Parroquia', max_length=20)
    dpa_despar = models.CharField('Nombre', max_length=40)
    dpa_canton = models.CharField('Canton', max_length=20)
    dpa_provin = models.CharField('Cod. Provincia', max_length=20)
    dpa_despro = models.CharField('Provincia', max_length=40)
    dpa_descan = models.CharField('Canton', max_length=40)
    mpoly = models.MultiPolygonField('Mapa Parroquial')
    objects = models.GeoManager()

    class Meta:
        verbose_name = ('Parroquia')
        verbose_name_plural = ('Parroquias del Azuay')

    def to_json(self):
        return '%s' % self.dpa_despar

#    def __unicode__(self):
#        return 'Canton: %s - %s' % (self.dpa_parroq, self.dpa_despar)
    
    def __str__(self):
        return '%s' % str(self.dpa_despar)

class Emprendimiento(models.Model):

    fields_popup = 'nombre','organization'

    mapping = {
        'nombre': 'nombre',
        'provincia': 'provincia',
        'point': 'POINT',
    }


    nombre = models.CharField(max_length=254, verbose_name='Nombre')
    representante = models.ForeignKey(Representante, verbose_name='Representante')
    num_socios = models.IntegerField(verbose_name='Numero de Socios')
    num_acuerdo_min = models.CharField('Acuerdo Ministerial',max_length=50, null=True, blank=True)
    activity = models.ForeignKey(Activity, verbose_name='Actividad')
    productos = models.ManyToManyField(Product, verbose_name='Productos', null=True, blank=True)
    productos_json = models.CharField(max_length=254)
    area_produccion = models.FloatField(verbose_name='Area de Produccion', null=True, blank=True)
    area_procesamiento = models.CharField(verbose_name='Lugar de Procesamiento', max_length=100, blank=True)
    ubicaciones = models.ManyToManyField(Ubicacion, verbose_name='Gente de Lugares')
    ubicaciones_json = models.CharField(max_length=254)
    parroquia = models.ForeignKey(Parroquia, verbose_name='Parroquia')
    canton = models.ForeignKey(Canton, verbose_name= u'Cantón')
    phone = models.CharField('Telefono', max_length=20, null=True, blank=True)
    info = models.TextField('Info Adicional', blank=True)
    point = models.PointField(verbose_name='Ubicacion en el Mapa')
    url_info = models.URLField(verbose_name='Sitio')
    tipomodel = models.CharField(max_length=20, default='emprendimiento')
    objects = models.GeoManager()

    def m2m_tojson(self):
        prods = self.productos.all()
        self.productos_json = ', '.join([item.name for item in prods])
        ubics = self.ubicaciones.all()
        self.ubicaciones_json = ', '.join([item.nombre for item in ubics])

    class Meta:
        verbose_name = 'Emprendimiento'
        verbose_name_plural = 'Emprendimientos'
    
    def __unicode__(self):
        return self.nombre

    def __str__(self):
        return '%s' % 'Emprendimiento'


class TipoActor(models.Model):
    nombre = models.CharField(max_length=50, verbose_name='Nombre')
    codigo = models.CharField(max_length=20, verbose_name=u'Código')
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.nombre    

    def __unicode__(self):
        return '%s' % self.nombre

    def to_json(self):
        return '%s' % self.nombre    

    class Meta:
        verbose_name = 'Tipo de Entidad'
        verbose_name_plural = 'Tipos de Entidades'


class Actor(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    direccion = models.CharField(max_length=200, verbose_name= u'Información')
    tipo = models.ForeignKey(TipoActor)
    url_info = models.URLField(verbose_name='Sitio', blank=True)
    tecnicos = models.ManyToManyField(Representante, verbose_name = 'Tecnicos')
    tecnicos_json = models.CharField(max_length=254)
    tipomodel = models.CharField(max_length=20, default='actor')
    poly = models.PointField('Area de Ubicacion')
    objects = models.GeoManager()


    def m2m_tojson(self):
        prods = self.tecnicos.all()
        self.tecnicos_json = ', '.join(['%s %s' % (item.first_name,item.last_name) for item in prods])

    def __str__(self):
        return '%s' % self.nombre

    def __unicode__(self):
        return '%s' % self.nombre  

    class Meta:
        verbose_name = 'Entidad'
        verbose_name_plural = 'Entidades'

#class PAManager(models.Manager):
#    use_for_related_fields = True

#    def to_json(self):
#        prods = self.get_query_set().filter(nombre<>'')
#        return ', '.join([item.nombre for item in prods])    

class ProductivityArea(models.Model):

    nombre = models.CharField(max_length=200, verbose_name='Nombre')
    actividad = models.ForeignKey(Activity, verbose_name='Actividad')
    productos = models.ManyToManyField(Product, verbose_name='Productos', blank=True)
    productos_json = models.CharField(max_length=254)
    parroquias = models.ManyToManyField(Parroquia, verbose_name='Parroquias', blank=True)
    parroquias_json = models.CharField(max_length=254)
    poly = models.MultiPolygonField('Zona Productiva')
    tipomodel = models.CharField(max_length=12, default='zonaprod')
    objects = models.GeoManager()


    def __str__(self):
        return '%s' % self.nombre

    def m2m_tojson(self):
        prods = self.productos.all()
        self.productos_json = ', '.join([item.name for item in prods])
        parroquias = self.parroquias.all()
        self.parroquias_json = ', '.join([item.dpa_despar for item in parroquias])

    class Meta:
        verbose_name = 'Area Productiva'
        verbose_name_plural = 'Areas Productivas'


class Provincia(models.Model):
    mapping = {
        'dpa_prov': 'DPA_PROVIN',
        'dpa_despro': 'DPA_DESPRO',
        'area': 'area',
        'mpoly': 'POLYGON',
        }
    
    dpa_prov = models.CharField('Codigo de Provincia', max_length=20)
    dpa_despro = models.CharField('Provincia', max_length=40)
    area = models.DecimalField('Area', max_digits=10, decimal_places=2)
    mpoly = models.MultiPolygonField('Mapa Provincial')
    objects = models.GeoManager()
    
    class Meta:
        verbose_name = ('Provincia')
        verbose_name_plural = ('Provincias del Ecuador')

    def __unicode__(self):
        return u'Provincia: %s - %s' % (self.dpa_despro, self.dpa_prov)



    


