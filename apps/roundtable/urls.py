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
    url(r'^process_search$', views.process_search),
    url(r'^process_vote$', views.process_vote),
    url(r'^link_restaurant/(?P<event_id>\d+)$', views.link_restaurant),
    url(r'^link_guest/(?P<event_id>\d+)$', views.link_guest),
    url(r'^process_update/(?P<event_id>\d+)$', views.process_update),
    url(r'^events/edit/(?P<event_id>\d+)$', views.editevent),
    url(r'^invite/(?P<event_id>\d+)$', views.handle_invite),
    url(r'^handle_accept/(?P<event_id>\d+)$', views.handle_accept),
]
