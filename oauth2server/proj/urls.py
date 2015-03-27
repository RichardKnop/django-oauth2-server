from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    '',
    url(r'^api/v1/', include('apps.tokens.urls', namespace='api_v1')),
    url(r'^web/', include('apps.web.urls', namespace='web')),
)