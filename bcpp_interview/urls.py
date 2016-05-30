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

urlpatterns = [
    url(r'login', LoginView.as_view(), name='login_url'),
    url(r'logout', LogoutView.as_view(pattern_name='login_url'), name='logout_url'),
    url(r'^transcribe/', TranscribeView.as_view(), name='transcribe'),
    url(r'^translate/', TranslateView.as_view(), name='translate'),
    url(r'^statistics/', StatisticsView.as_view(), name='update-statistics'),
    url(r'^call_manager/$', RedirectView.as_view(pattern_name='home')),
    url(r'^call_manager/', include('edc_call_manager.urls', 'call_manager')),
    url(r'^recording/$', RedirectView.as_view(url='/')),
    url(r'^recording/', include('audio_recording.urls')),
    url(r'^sync/$', RedirectView.as_view(url='/')),
    url(r'^sync/', include('edc_sync.urls')),
    url(r'^encryption/$', RedirectView.as_view(url='/')),
    url(r'^encryption/', encryption_admin.urls),
    url(r'^admin/import/(?P<app_label>\w+)/(?P<model_name>\w+)/',
        ImportDataView.as_view(), {'app_label': 'bcpp_interview', 'model_name': 'potential_subject'},
        name='import_potential_subjects'),
    url(r'^admin/$', RedirectView.as_view(url='/')),
    url(r'^admin/', call_manager_admin.urls),
    url(r'^admin/', admin.site.urls),
    url(r'^home/', HomeView.as_view(), name='home'),
    url(r'^', HomeView.as_view(), name='home'),
]

admin.site.site_header = 'BCPP Interview'
admin.site.site_title = 'BCPP Interview'
admin.site.index_title = 'BCPP Interview Admin'
admin.site.site_url = '/admin/bcpp_interview/'
