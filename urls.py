"""
Definition of urls for DjangoPYtest.
"""

from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from dapp import views
import dapp

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', 'DjangoPYtest.views.home', name='home'),
    # url(r'^DjangoPYtest/', DjangoPYtest.DjangoPYtest.urls),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', admin.site.urls),
    url(r'^index/$',dapp.views.hello),
    url(r'^consult/([a-z]*)/$',dapp.views.consult),
    url(r'^register/(.*)/$',dapp.views.register),
    url(r'^connectiontest/$',dapp.views.connectiontest),
    url(r'^mission/(.*)/$',dapp.views.opreate),
    url(r'^ifexist/(.*)/$',dapp.views.ifexist),
    url(r'^login/(.*)/$',dapp.views.login),
]
