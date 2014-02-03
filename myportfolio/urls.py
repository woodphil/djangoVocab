"""PROJECT URLS"""
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'myportfolio.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

	url(r'^', include('portfolioSite.urls')),
	url(r'^projects/vocabtest/', include('vocabTest.urls')),
	#url(r'^', include('django.contrib.flatpages.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
