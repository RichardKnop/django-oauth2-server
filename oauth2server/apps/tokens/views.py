from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator

from apps.tokens.serializers import OAuthAccessTokenSerializer
from apps.tokens.decorators import validate_request
from apps.tokens.granttypes import factory


class TokensView(APIView):

    @method_decorator(validate_request)
    def post(self, request, *args, **kwargs):
        access_token = factory(request=request).grant()
        return Response(
            OAuthAccessTokenSerializer(access_token).data,
            status=status.HTTP_201_CREATED,
        )