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
from picbackend import views
from presencescheduler import urls as scheduler_urls

#enables admin
admin.autodiscover()

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

    url(r'^', include(scheduler_urls)),
    url(r"^$", views.index),
    url(r"^submitmetrics/$", views.metrics_submission_handler),
    url(r"^editstaff/$", views.staff_edit_handler),
    url(r"^editconsumer/$", views.consumer_edit_handler),
    url(r"^v1/staff$", views.staff_api_handler),
    url(r"^v1/consumers$", views.consumer_api_handler),
    url(r"^v1/metrics$", views.metrics_api_handler),
    url(r"^v1/eligibility", views.eligibility_handler),
    url(r"^v1/tradingpartners", views.trading_partner_handler),
    url(r'^admin/', include(admin.site.urls)),
]
