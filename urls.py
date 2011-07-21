from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('gallery.views',
    (r'^$', 'index'),
    (r'^album/(?P<album_id>\d+)/$', 'album'),
)
