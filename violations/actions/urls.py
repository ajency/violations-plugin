from django.conf.urls import url
from actions import views

urlpatterns = [
    url(r'^view/$', views.ViewActionData.as_view(), name="actions.view"),
    url(r'^add/$', views.SetActionData.as_view(), name="actions.add"),
]