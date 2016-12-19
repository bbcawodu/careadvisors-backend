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

from django.contrib.auth.views import login
from django.views.generic import TemplateView

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
    url(r"^submitmetrics/$", views.handle_metrics_submission_request),
    url(r"^editstaff/$", views.handle_staff_edit_request),
    url(r"^addlocation/$", views.handle_location_add_request),
    url(r"^managelocations/$", views.handle_manage_locations_request),
    url(r"^editconsumer/$", views.handle_consumer_edit_request),
    url(r"^edithublocation/$", views.handle_hub_location_edit_api_request),
    url(r"^v1/staff/$", views.handle_staff_api_request),
    url(r"^v1/consumers/$", views.handle_consumer_api_request),
    url(r"^v1/metrics/$", views.handle_metrics_api_request),
    url(r"^v1/eligibility/$", views.handle_eligibility_request),
    url(r"^v1/tradingpartners/$", views.handle_trading_partner_request),
    url(r"^v1/navlocations/$", views.handle_nav_location_api_request),
    url(r"^v1/getnavappointments/$", views.handle_nav_appointments_api_request),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^oauth2callback', views.auth_return),
    url(r"^accounts/login/$", login, {'template_name': 'login.html'}),
    url(r"^v1/calendar_auth/$", views.handle_calendar_auth_request),
    url(r"^v1/viewscheduledappointments/$", views.handle_view_sched_apt_request),
    url(r"^v1/add_consumer_appointment_with_nav/$", views.handle_add_consumer_apt_with_nav_request),
    url(r"^v1/delete_consumer_appointment_with_nav/$", views.handle_delete_consumer_apt_with_nav_request),
    url(r'^google2a62fdb4823a96c9.html$', TemplateView.as_view(template_name="google2a62fdb4823a96c9.html"), name='google2a62fdb4823a96c9'),
]
