from django.conf.urls.defaults import url, include, patterns
from django.contrib import admin
__author__ = 'sreeraj'


urlpatterns = patterns('trip.views',
    # Examples:
    # url(r'^$', 'backend.views.home', name='home'),
    # url(r'^backend/', include('backend.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/user/', include('backend.users.urls')),
)
