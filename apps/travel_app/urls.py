from django.conf.urls import url
import views
urlpatterns = [
    url(r'^main$', views.main),
    url(r'^register$', views.register),
    url(r'^travels$', views.travels),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^travels/add$', views.addingplan),
    url(r'^addplan$', views.addplan),
    url(r'^show/(?P<travel_id>\d+)$', views.show),
    url(r'^delete/(?P<id>\d+)$', views.delete),
    url(r'^join/(?P<travel_id>\d+)$', views.join),
]
