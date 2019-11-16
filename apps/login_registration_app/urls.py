from django.conf.urls import url
from . import views
urlpatterns=[
    url(r'^$' , views.index),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^profile$', views.profile),
    url(r'^logout$', views.logout),
    url(r'^trip/add$', views.add_trip),
    url(r'^trip/create$', views.create_trip),
    url(r'^trip/edit/(?P<trip_id>\d+)$', views.edit_trip),
    url(r'^trip/edit/(?P<trip_id>\d+)/create$', views.edit_trip_create),
    url(r'^trip/(?P<trip_id>\d+)$', views.view_trip),
    url(r'^trip/(?P<trip_id>\d+)/join$', views.join_trip),
    url(r'^trip/(?P<trip_id>\d+)/cancel$', views.cancel_trip),
    url(r'^trip/(?P<trip_id>\d+)/delete$', views.trip_delete)
]