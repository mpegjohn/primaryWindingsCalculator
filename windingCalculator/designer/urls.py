from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'wire/$', views.wire_size, name='wire_size'),
]
