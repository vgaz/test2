from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^var/', 'main.views.var', name='tab_varietes'),
    # url(r'^home/', include('blog.urls')),
    url(r'^quiz/', 'main.views.quiz', name='quiz'),
    url(r'^planche/', 'main.views.planche', name='planche'),
    url(r'^$', 'main.views.home', name='home'),


    url(r'^admin/', include(admin.site.urls)),
)
