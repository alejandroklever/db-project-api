import os

# For Downloading Files
from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from rest_framework import filters
from rest_framework.viewsets import ModelViewSet

import apps.revista_cientifica.models as models
import apps.revista_cientifica.serializers as serializers


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['^username', '^first_name', '^last_name']


class AuthorViewSet(ModelViewSet):
    queryset = models.Author.objects.all()
    serializer_class = serializers.AuthorSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['^user__username', '^user__first_name', '^user__last_name']


class NotificationViewSet(ModelViewSet):
    queryset = models.Notification.objects.all()
    serializer_class = serializers.NotificationSerializer


class MCCViewSet(ModelViewSet):
    queryset = models.MCC.objects.all()
    serializer_class = serializers.MCCSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['^id', '^area']


class ArticleViewSet(ModelViewSet):
    queryset = models.Article.objects.all()
    serializer_class = serializers.ArticleSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['^title', '^keywords', '^author__user__username']


class ParticipationViewSet(ModelViewSet):
    queryset = models.Participation.objects.all()
    serializer_class = serializers.ParticipationSerializer


class RefereeViewSet(ModelViewSet):
    queryset = models.Referee.objects.all()
    serializer_class = serializers.RefereeSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['^user__username', '^user__first_name', '^user__last_name']


class ArticleInReviewViewSet(ModelViewSet):
    queryset = models.ArticleInReview.objects.all()
    serializer_class = serializers.ArticleSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['^article__title', '^referee__user__username']


class FileViewSet(ModelViewSet):
    queryset = models.File.objects.all()
    serializer_class = serializers.FileSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['^file_name', '^article__title']


def download_file(request, path: str) -> HttpResponse:
    file_path = os.path.join(settings.BASE_DIR, 'apps', 'revista_cientifica', 'media', path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="text/plain")
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            return response
    raise Http404()
