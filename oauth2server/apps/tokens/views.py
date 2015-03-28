from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator

from apps.tokens.serializers import OAuthAccessTokenSerializer
from apps.tokens.decorators import (
    client_credentials_required,
    grant_type_required,
)
from apps.tokens.granttypes import factory


class TokensView(APIView):

    @method_decorator(client_credentials_required)
    @method_decorator(grant_type_required)
    def post(self, request, *args, **kwargs):
        access_token = grant_instance = factory(
            grant_type=request.grant_type,
            client=request.client,
            request=request,
        ).grant()
        return Response(
            OAuthAccessTokenSerializer(access_token).data,
            status=status.HTTP_201_CREATED,
        )