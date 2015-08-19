from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from cards import views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', include('cards.urls')),
    url(r'^search/', include('haystack.urls')),
    url(r'^om/$', views.about, name='about'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^(?P<catalog_slug>[a-z]+)/(?P<card_catalog_sequence_number>[0-9a-z]+)/$', views.browse, name='cardurl'),
)
