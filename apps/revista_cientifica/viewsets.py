import os

# For Downloading Files
from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, status
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response

import apps.revista_cientifica.models as models
import apps.revista_cientifica.serializers as serializers


class UserViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    filter_backends = [filters.SearchFilter]
    search_fields = ['^username', '^first_name', '^last_name']
    serializer_class = serializers.CreateUserSerializer
    queryset = User.objects.all()

    def list(self, request, *args, **kwargs):
        self.queryset = User.objects.all()
        serializer = serializers.UserReadOnlySerializer(self.queryset, many=True)
        return Response(serializer.data)


class DetailUserViewSet(mixins.DestroyModelMixin,
                        GenericViewSet):
    serializer_class = serializers.DetailUserSerializer
    queryset = User.objects.all()

    def retrieve(self, request, pk=None, *args, **kwargs):
        user = get_object_or_404(self.queryset, pk=pk)
        serializer = serializers.UserReadOnlySerializer(user)
        return Response(serializer.data)


class UpdateUserViewSet(mixins.UpdateModelMixin,
                        GenericViewSet):
    serializer_class = serializers.UpdateUserSerializer
    queryset = User.objects.all()


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

    def destroy(self, request, *args, **kwargs):
        f = get_object_or_404(self.queryset, pk=kwargs['pk'])
        path = os.path.join(settings.BASE_DIR, f.file.name)
        os.remove(path)
        f.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        f = get_object_or_404(self.queryset, pk=kwargs['pk'])
        path = os.path.join(settings.BASE_DIR, f.file.name)
        try:
            response = super().update(request, *args, **kwargs)
            os.remove(path)
            return response
        except Exception as e:
            raise e


def download_file(request, path: str) -> HttpResponse:
    file_path = os.path.join(settings.BASE_DIR, 'apps', 'revista_cientifica', 'media', path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="text/plain")
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            return response
    raise Http404()
