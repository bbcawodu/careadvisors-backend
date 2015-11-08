"""picproject URL Configuration

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
from django.conf.urls import patterns, include, url
from django.contrib import admin
from picproject import views

#enables admin
# admin.autodiscover()

urlpatterns = [
	# Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    # url(r'^admin/', include(admin.site.urls)),
    # urlconfig for homepage
    #url(r'^$', my_homepage_view),
    url(r"^$", views.index),
    url(r'^hello/$', views.hello),
    url(r'^time/$', views.current_datetime),
    #any numbuer of digits for plus argument
    #url(r'^time/plus/(\d+)/$', hours_ahead),
    #only 1 or 2 digits for plus argument
    url(r'^time/plus/(\d{1,2})/$', views.hours_ahead),
    url(r'^search-form/$', views.search_form),
    url(r'^search/$', views.search),
    url(r'^registration/$', views.registration),
    url(r'^memberlist/$', views.memberlist),
    url(r"^riskassessment/$", views.risk_assessment),
    url(r"^riskassessment/next/$", views.risk_assessment_2)
]
