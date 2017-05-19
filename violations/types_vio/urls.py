from django.conf.urls import url
from types_vio import views

urlpatterns = [
    url(r'^view/$', views.view_types, name="types_vio.view"),
    url(r'^add/$', views.violation_types, name="types_vio.add"),
]