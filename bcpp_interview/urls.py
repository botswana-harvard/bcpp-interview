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
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic.base import RedirectView
from django_crypto_fields.admin import encryption_admin

from edc_base.views import LoginView, LogoutView
from edc_call_manager.admin import call_manager_admin

from .views import (
    HomeView, StatisticsView, LocationView)

urlpatterns = [
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'login', LoginView.as_view(), name='login_url'),
    url(r'logout', LogoutView.as_view(pattern_name='login_url'), name='logout_url'),
    url(r'^statistics/', StatisticsView.as_view(), name='update-statistics'),
    url(r'^call_manager/$', RedirectView.as_view(pattern_name='home')),
    url(r'^call_manager/', include('edc_call_manager.urls', 'call_manager')),
    url(r'^recording/$', RedirectView.as_view(pattern_name='home')),
    url(r'^recording/', include('audio_recording.urls')),
    url(r'^sync/$', RedirectView.as_view(url='/')),
    url(r'^sync/', include('edc_sync.urls')),
    # url(r'^map/', include('edc_map.urls')),
    url(r'^map/$', RedirectView.as_view(pattern_name='home')),
    url(r'^map/(?P<map_area>\w+)/(?P<subject_identifier>[0-9\-]{14})/', LocationView.as_view(), name='location_url'),
    url(r'^admin/$', RedirectView.as_view(url='/')),
    url(r'^admin/', encryption_admin.urls),
    url(r'^admin/', call_manager_admin.urls),
    url(r'^admin/', admin.site.urls),
    url(r'^home/', HomeView.as_view(), name='home'),
    url(r'^', HomeView.as_view(), name='home'),
]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_header = 'BCPP Interview'
admin.site.site_title = 'BCPP Interview'
admin.site.index_title = 'BCPP Interview Admin'
admin.site.site_url = '/admin/bcpp_interview/'
