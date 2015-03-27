from rest_framework import serializers

from apps.tokens.models import OAuthAccessToken


class OAuthAccessTokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = OAuthAccessToken
        fields = (
            'id',
            'access_token',
            'expires_at',
            'token_type',
            'scope',
        )