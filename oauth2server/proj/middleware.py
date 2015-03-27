from django.http import HttpResponseBadRequest
from rest_framework.response import Response


class JSONExceptionMiddleware(object):
    def process_exception(self, request, exception):
        if isinstance(exception, HttpResponseBadRequest):
            return Response(data={
                'error': u'invalid_request',
                'error_description': unicode(exception),
            }, status=400)

        return Response(data={
            'error': u'server_error',
            'error_description': unicode(exception),
        }, status=500)