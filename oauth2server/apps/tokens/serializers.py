from rest_framework import serializers

from apps.tokens.models import OAuthAccessToken


class OAuthAccessTokenSerializer(serializers.ModelSerializer):

    refresh_token = serializers.CharField(
        source='refresh_token.refresh_token')

    class Meta:
        model = OAuthAccessToken
        fields = (
            'id',
            'access_token',
            'expires_at',
            'token_type',
            'scope',
            'refresh_token',
        )