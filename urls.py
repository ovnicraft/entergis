from django.conf.urls.defaults import *
from django.conf import settings
from entergis.views import homepage

# enable the admin:
from django.contrib import admin
admin.autodiscover()

#if settings.DEBUG:
#    urlpatterns = patterns('',
#        (r'^site_media(?P<path>.*)$', 'django.views.static.serve', {#
#        'document_root': })
#    print settings.STATIC_MEDIA
#else:
#    urlpatterns = patterns('')

urlpatterns = patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': settings.STATIC_MEDIA}),
    (r'^gis/entergis/', include('entergis.urls')),
    (r'^gis/admin/', include(admin.site.urls)),
    (r'^$', homepage),
)


