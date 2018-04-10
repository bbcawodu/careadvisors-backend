"""
picbackend URL Configuration

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


from django.conf.urls import include
from django.conf.urls import url
from django.contrib import admin
from picbackend import views
from presencescheduler import urls as scheduler_urls
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

# enables django admin page
admin.autodiscover()

# defines mappings from url patterns to views
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

    # include urls that are defined in the presencescheduler app
    url(r'^', include(scheduler_urls)),

    # url for index view
    url(r"^$", views.index),

    # url for django admin page
    url(r'^admin/', include(admin.site.urls)),

    # urls used to validate our application with Google. DO NOT REMOVE or API calls might be rejected
    url(r'^google2a62fdb4823a96c9.html$', TemplateView.as_view(template_name="google2a62fdb4823a96c9.html"), name='google2a62fdb4823a96c9'),


    ###################
    #API Version 2 URLS
    ###################

    # urls for navigators views
    url(r"^v2/navigators/$", views.NavigatorManagementView.as_view()),
    url(r"^v2/navigator_sign_up/$", views.NavigatorSignUpView.as_view()),
    url(r"^v2/navigator_pic/$", views.upload_navigator_pic),
    url(r"^v2/nav_resume/$", views.upload_nav_resume),

    # urls for navigator organizations from care advisors form views
    url(r"^v2/nav_orgs_from_form/$", views.NavOrgsFromOnlineFormMgmtView.as_view()),

    # urls for consumer views
    url(r"^v2/consumers/$", views.ConsumerManagementView.as_view()),
    url(r"^v2/backup_consumers/$", views.ConsumerBackupManagementView.as_view()),

    # urls for consumer metrics views
    url(r"^v2/metrics/$", views.ConsumerMetricsManagementView.as_view()),

    # urls for location views
    url(r"^v2/navigator_hub_locations/$", views.NavHubLocationManagementView.as_view()),

    # urls for consumer health insurance views
    url(r"^v2/consumer_health_insurance_benefits/$", views.ConsumerHealthInsuranceBenefitsView.as_view()),
    url(r"^v2/health_insurance_trading_partners/$", views.TradingPartnerView.as_view()),

    # urls for patient assist scheduler views
    url(r"^v2/calendar_auth/$", views.NavGoogleCalendarAccessRequestView.as_view()),
    url(r'^v2/oauth2callback', views.GoogleCalendarAuthReturnView.as_view()),
    url(r'^v2/patient_assist_apt_mgr', views.PatientAssistAptMgtView.as_view()),

    # urls for call to action views
    url(r"^v2/cta_management/$", views.manage_cta_request),
    url(r"^v2/cta/$", views.ViewCTAView.as_view()),

    # urls for provider network and accepted plans views
    url(r"^v2/carriers/$", views.CarriersManagementView.as_view()),
    url(r"^v2/carrier_sample_id_card_manager/$", views.handle_carrier_sample_id_card_mgmt_rqst),
    url(r"^v2/plans/$", views.PlansManagementView.as_view()),
    url(r"^v2/provider_locations/$", views.ProviderLocationsManagementView.as_view()),
    url(r"^v2/provider_networks/$", views.ProviderNetworksManagementView.as_view()),

    # urls for patient story concerns views
    url(r"^v2/general_concerns/$", views.GeneralConcernsManagementView.as_view()),
    url(r"^v2/specific_concerns/$", views.SpecificConcernsManagementView.as_view()),
    url(r"^v2/ranked_specific_concerns/$", views.RankedSpecificConcernsView.as_view()),

    # urls for hospital web traffic calculator views
    url(r"^v2/hospital_web_traffic_data/$", views.HospitalWebTrafficCalculatorDataMgrView.as_view()),

    # urls for Healthcare Subsidy Eligibility Data By Family Size views
    url(r"^v2/subsidy_data_by_family_size/$", views.HealthcareSubsidyEligibilityDataMgrView.as_view()),

    # urls for Care Advisor customer views
    url(r"^v2/care_advisor_customer/$", views.CareAdvisorCustomerMgmtView.as_view()),

    # dashboard urls
    url(r"^v2/dashboard/$", views.DashboardView.as_view()),
    url(r"^v2/dashboard_demo/$", views.v2.render_demo_dashboard),

    # healthcare service expertise urls
    url(r'v2/service_expertise/$', views.ServiceExpertiseManagementView.as_view()),

    # healthcare service expertise urls
    url(r'v2/marketplace_appointments/$', views.MarketplaceAppointmentManagementView.as_view()),


    ###################
    #CPS API V1 URLS
    ###################

    # urls for staff views
    url(r"^cps/v1/staff/$", views.cps.CPSStaffManagementView.as_view()),
    url(r"^cps/v1/staff_pic/$", views.cps.upload_cps_staff_pic),

    # urls for cps metrics views
    url(r"^cps/v1/metrics/$", views.cps.CPSMetricsManagementView.as_view()),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
