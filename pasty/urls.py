from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'core.views.home', name='home'),
    url(r'^one$', 'core.views.one', name='one'),
    url(r'^sources$', 'core.views.sources', name='sources'),
    url(r'^sync$', 'core.views.sync', name='sync'),
    # url(r'^pasty/', include('pasty.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
