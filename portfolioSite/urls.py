'''MAINPORTFOLIOSITE URLS'''

from django.conf.urls import patterns, url

from portfolioSite import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
	url(r'^resume/$', views.resume, name='resume'),
	url(r'^projects/$', views.projects, name='projects'),
	url(r'^contact/$', views.contact, name='contact'),
)