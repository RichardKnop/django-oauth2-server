from django.conf.urls import url

from apps.web.views import AuthorizeView


urlpatterns = [
    url('^authorize/?', AuthorizeView.as_view(), name='authorize'),
]