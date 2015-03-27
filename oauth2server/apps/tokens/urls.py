from django.conf.urls import patterns, url

from apps.tokens.views import TokensView


urlpatterns = patterns(
    '',
    url('^tokens/?', TokensView.as_view(), name='tokens'),
)