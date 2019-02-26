from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^dashboard$', views.dashboard),
    url(r'^events/new$', views.createevent),
    # url(r'^jobs/edit/(?P<job_id>\d+)$', views.editjob),
    # url(r'^jobs/(?P<job_id>\d+)$', views.viewjob),
    # url(r'^process_addjob$', views.process_addjob),
    url(r'^process_register$', views.process_register),
    url(r'^process_logout$', views.process_logout),
    url(r'^process_login$', views.process_login),
    # url(r'^process_update/(?P<job_id>\d+)$', views.process_update),
    # url(r'^process_delete/(?P<job_id>\d+)$', views.process_delete),
    # url(r'^process_takejob/(?P<job_id>\d+)$', views.process_takejob),
    # url(r'^process_giveupjob/(?P<job_id>\d+)$', views.process_giveupjob),

]

