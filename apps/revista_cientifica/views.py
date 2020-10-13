import os

from django.conf import settings
from django.http import HttpResponse, Http404
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

import apps.revista_cientifica.models as models
from apps.revista_cientifica.serializers import UserInfoSerializer
from apps.revista_cientifica.tools.documents import generate_document


class UserAuthView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(UserAuthView, self).post(request, *args, **kwargs)
        token = response.data['token']
        user = Token.objects.get(key=token).user
        response.data.update(UserInfoSerializer(user).data)
        return response


def download_file(request, path: str):
    file_path = os.path.join(settings.BASE_DIR, 'apps', 'revista_cientifica', 'media', 'file', path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="text/plain")
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            return response
    raise Http404()


def download_report(request, pk: int):
    notification = models.Notification.objects.get(id=pk)
    author = models.Author.objects.get(user=notification.user)
    file_path = generate_document(str(author), author.institution, notification.content, notification.date)
    with open(file_path, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/msword")
        response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
        os.remove(file_path)
        return response
