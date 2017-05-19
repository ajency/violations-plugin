"""violations URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin


from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

from .views import violation_data, ViolationData

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)


urlpatterns = [
	url(r'^', include(router.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

	url(r'^types/', include('types_vio.urls'), name='violations.types'), ## -- Link to Types urls.py -- ##
    
    #url(r'^violations/$', ViolationData.as_view()), ## -- Link to Violation functions -- ##
    url(r'^violations/', violation_data, name='violations.violation'), ## -- Link to Violation functions -- ##
    
    url(r'^actions/', include('actions.urls'), name='violations.actions'), ## -- Link to Actions urls.py -- ##
    url(r'^comments/', include('comments.urls'), name='violations.comments'), ## -- Link to Comments urls.py -- ##

]