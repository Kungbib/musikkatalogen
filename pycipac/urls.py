from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from cards import views

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pycipac.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', include('cards.urls')),
    url(r'^search/$', views.search, name='search'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^(?P<catalog_slug>[a-z]+)/(?P<box_sequence_number>\d+)/(?P<card_catalog_sequence_number>[0-9a-z]+)/$', views.browse, name='cardurl'),
    #url(r'^card/([0-9]+)/$', views.browse, name='browse'),
)
