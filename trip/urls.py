from django.conf.urls.defaults import url, include, patterns

__author__ = 'sreeraj'


urlpatterns = patterns('trip.views',
    # Examples:
    # url(r'^$', 'backend.views.home', name='home'),
    # url(r'^backend/', include('backend.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^get-nearby-places/(?P<place_name>[a-zA-Z]*)/$', 'get_nearby_places'),
    url(r'^api/log-events/$','create_log_entry'),
    url(r'create-trip/','trip_planner')
)
