from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'wire/$', views.wire_size, name='wire_size'),
    url(r'inductor/$', views.inductor, name='inductor'),
    url(r'laminations/$', views.laminations, name='laminations'),
    url(r'laminations/edit/(?P<id>\d+)$', views.edit_lamination),
    url(r'laminations/update/(?P<id>\d+)$', views.update_lamination),
    url(r'laminations/delete/(?P<id>\d+)$', views.delete_lamination, name='delete_lamination'),
    url(r'cores/$', views.cores, name='cores'),
    url(r'cores/edit/(?P<id>\d+)$', views.edit_cores),
    url(r'cores/update/(?P<id>\d+)$', views.update_cores),
    url(r'cores/delete/(?P<id>\d+)$', views.delete_cores, name='delete_cores'),
    url(r'bobbins/$', views.bobbins, name='bobbins'),

]
