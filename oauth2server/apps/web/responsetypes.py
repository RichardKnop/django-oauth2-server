import urllib
import uuid

from django.http import HttpResponseRedirect

from apps.tokens.models import (
    OAuthAuthorizationCode,
    OAuthAccessToken,
)


def factory(response_type):
    return {
        'code': CodeResponseType(),
        'token': ImplicitResponseType(),
    }[response_type]


class AbstractResponseType(object):

    def denied_redirect(self, state, redirect_uri):
        query_string = urllib.urlencode({
            'error': u'access_denied',
            'error_description': u'The user denied access to your application',
            'state': state,
        })

        return HttpResponseRedirect('{}?{}'.format(
            redirect_uri, query_string))


class CodeResponseType(AbstractResponseType):

    def process(self, client, authorized, scopes, redirect_uri, state):
        if not authorized:
            return self.denied_redirect(
                state=state, redirect_uri=redirect_uri)

        auth_code = OAuthAuthorizationCode.objects.create(
            code=unicode(uuid.uuid4()),
            expires_at=OAuthAuthorizationCode.new_expires_at(),
            client=client,
            redirect_uri=redirect_uri,
        )
        auth_code.scopes.add(*scopes)

        query_string = urllib.urlencode({
            'code': auth_code.code,
            'state': state,
        })

        return HttpResponseRedirect('{}?{}'.format(
            redirect_uri, query_string))


class ImplicitResponseType(AbstractResponseType):

    def process(self, client, authorized, scopes, redirect_uri, state):
        if not authorized:
            return self.denied_redirect(
                state=state, redirect_uri=redirect_uri)

        access_token = OAuthAccessToken.objects.create(
            access_token=unicode(uuid.uuid4()),
            expires_at=OAuthAccessToken.new_expires_at(),
            client=client,
        )
        access_token.scopes.add(*scopes)

        return HttpResponseRedirect(
            '{}#access_token={}&expires_in={}'
            '&token_type=Bearer&state={}'.format(
                redirect_uri, access_token.access_token,
                access_token.expires_in, state,
        ))