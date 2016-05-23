"""bcpp_interview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic.base import RedirectView
from django_crypto_fields.admin import encryption_admin
from edc_call_manager.admin import call_manager_admin

from .views import (
    HomeView, LoginView, LogoutView, TranscribeView, TranslateView, StatisticsView, ImportDataView)
from bcpp_interview.views.call_subject_view import CallSubjectView

urlpatterns = [
    url(r'^admin/logout/', LogoutView.as_view(url='/login/')),
    url(r'^login/', LoginView.as_view(), name='login_url'),
    url(r'^logout/', LogoutView.as_view(url='/login/'), name='logout_url'),
    url(r'^accounts/login/', LoginView.as_view()),
    url(r'^home/', HomeView.as_view(), name='home'),
    url(r'^transcribe/', TranscribeView.as_view(), name='transcribe'),
    url(r'^translate/', TranslateView.as_view(), name='translate'),
    url(r'^statistics/', StatisticsView.as_view(), name='update-statistics'),
    url(r'^call_manager/$', RedirectView.as_view(url='/')),
    url(r'^call_manager/(?P<app_label>\w+)/(?P<model_name>\w+)/(?P<pk>[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12})/',
        CallSubjectView.as_view(), name='call_subject'),
    url(r'^call_manager/(?P<app_label>\w+)/(?P<model_name>\w+)/',
        CallSubjectView.as_view(), name='call_subject'),
    url(r'^call_manager/', include('edc_call_manager.urls')),
    url(r'^encryption/$', RedirectView.as_view(url='/')),
    url(r'^encryption/', encryption_admin.urls),
    url(r'^admin/import/(?P<app_label>\w+)/(?P<model_name>\w+)/',
        ImportDataView.as_view(), {'app_label': 'bcpp_interview', 'model_name': 'potential_subject'},
        name='import_potential_subjects'),
    url(r'^admin/cm/$', RedirectView.as_view(url='/')),
    url(r'^admin/cm/', call_manager_admin.urls),
    url(r'^admin/$', RedirectView.as_view(url='/')),
    url(r'^admin/', admin.site.urls),
    url(r'^recording/admin/$', RedirectView.as_view(url='/')),
    url(r'^recording/$', RedirectView.as_view(url='/')),
    url(r'^recording/', include('edc_audio_recording.urls')),
    url(r'^edc_sync/', include('edc_sync.urls')),
    url(r'', HomeView.as_view(), name='default'),
]

admin.site.site_header = 'BCPP Interview'
admin.site.site_title = 'BCPP Interview'
admin.site.index_title = 'BCPP Interview Admin'
admin.site.site_url = '/admin/bcpp_interview/'
