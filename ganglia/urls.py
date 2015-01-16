from django.conf.urls import patterns, url
from ganglia import views

urlpatterns = patterns('',
	url(r'^$',views.index,name='index'),
	url(r'^(?P<resource_id>\d+)/$', views.detail, name='detail'),
)
