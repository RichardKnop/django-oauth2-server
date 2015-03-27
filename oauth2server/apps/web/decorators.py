from django.http import Http404

from apps.credentials.models import OAuthClient


def client_required(view):
    def wrapper(request, *args, **kwargs):
        try:
            client = OAuthClient.objects.get(client_id=request.GET['client_id'])
        except (OAuthClient.DoesNotExist, KeyError):
            raise Http404(u'Client not found')

        request.client = client
        return view(request, *args, **kwargs)
    return wrapper