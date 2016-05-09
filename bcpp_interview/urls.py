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
from django.db.utils import OperationalError, ProgrammingError
from .edc_app_configuration import EdcAppConfiguration
from .views import (
    HomeView, LoginView, LogoutView, TranscribeView, TranslateView, RecordView)

try:
    edc_app_configuration = EdcAppConfiguration()
    edc_app_configuration.prepare()
except OperationalError as e:
    print('skipping edc configuration')
except ProgrammingError as e:
    print('skipping edc configuration')
    # pass

urlpatterns = [
    url(r'^admin/logout/', LogoutView.as_view(url='/login/')),
    url(r'^login/', LoginView.as_view(), name='login_url'),
    url(r'^logout/', LogoutView.as_view(url='/login/'), name='logout_url'),
    url(r'^accounts/login/', LoginView.as_view()),
    url(r'^home/', HomeView.as_view(), name='home'),
    url(r'^record/(?P<app_label>.*)/(?P<model_name>.*)/(?P<pk>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/', RecordView.as_view(), name='record'),
    url(r'^transcribe/', TranscribeView.as_view(), name='transcribe'),
    url(r'^translate/', TranslateView.as_view(), name='translate'),
    url(r'^admin/', admin.site.urls),
    url(r'^edc_sync/', include('edc_sync.urls')),
    url(r'', HomeView.as_view(), name='default'),
]

admin.site.site_header = 'BCPP Interview'
admin.site.site_title = 'BCPP Interview'
admin.site.index_title = 'BCPP Interview Admin'
admin.site.site_url = '/admin/bcpp_interview/'
