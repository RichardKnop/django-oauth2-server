import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.conf import settings

from apps.tokens.models import OAuthAccessToken
from apps.tokens.serializers import OAuthAccessTokenSerializer
from apps.tokens.decorators import (
    client_credentials_required,
    grant_type_required,
)


class TokensView(APIView):
    @method_decorator(client_credentials_required)
    @method_decorator(grant_type_required)
    def post(self, request, *args, **kwargs):
        if request.grant_type == 'client_credentials':
            return self._client_credentials(request=request)

    def _client_credentials(self, request):
        try:
            token_lifetime = settings.OAUTH2_SERVER['ACCESS_TOKEN_LIFETIME']
        except KeyError:
            token_lifetime = 3600
        access_token = OAuthAccessToken.objects.create(
            access_token=unicode(uuid.uuid4()),
            expires_at=timezone.now() + timezone.timedelta(seconds=token_lifetime),
            client=request.client,
        )
        return Response(OAuthAccessTokenSerializer(access_token).data, status=201)