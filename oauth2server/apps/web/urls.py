from django.conf.urls import patterns, url

from apps.web.views import AuthorizeView


urlpatterns = patterns(
    '',
    url('^authorize/?', AuthorizeView.as_view(), name='authorize'),
)