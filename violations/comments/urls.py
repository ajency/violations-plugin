from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns
from comments import views

urlpatterns = [
    url(r'^view/$', views.ViewCommentData.as_view(), name="comments.view"),
    url(r'^add/$', views.SetCommentData.as_view(), name="comments.add"),
]