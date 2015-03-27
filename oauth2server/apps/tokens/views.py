from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.decorators import method_decorator

from apps.tokens.serializers import OAuthAccessTokenSerializer
from apps.tokens.decorators import (
    client_credentials_required,
    grant_type_required,
)


class TokensView(APIView):

    @method_decorator(client_credentials_required)
    @method_decorator(grant_type_required)
    def post(self, request, *args, **kwargs):
        access_token = request.grant_type.grant()
        serialized_token = OAuthAccessTokenSerializer(access_token).data
        return Response(serialized_token, status=201)