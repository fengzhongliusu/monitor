from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'monitor.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^ganglia/', include('ganglia.urls',namespace="ganglia")),
    url(r'^admin/', include(admin.site.urls)),
)
