from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^dashboard$', views.dashboard),
    url(r'^events/new$', views.createevent),
    url(r'^process_register$', views.process_register),
    url(r'^process_logout$', views.process_logout),
    url(r'^process_login$', views.process_login),
    url(r'^process_addevent$', views.process_addevent),
    url(r'^process_delete/(?P<id>\d+)$', views.process_delete),
]
