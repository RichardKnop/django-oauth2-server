from django.conf.urls import url

from apps.tokens.views import TokensView


urlpatterns = [
    url('^tokens/?', TokensView.as_view(), name='tokens'),
]