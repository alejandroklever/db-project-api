import os

from django.conf import settings
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

import apps.revista_cientifica.filters as custom_filters
import apps.revista_cientifica.models as models
import apps.revista_cientifica.serializers as serializers
from apps.revista_cientifica.document_maker import generate_document
from apps.revista_cientifica.notifications_maker import NotificationMaker

notification_maker = NotificationMaker()


class UserAuthView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(UserAuthView, self).post(request, *args, **kwargs)
        token = response.data['token']
        user = Token.objects.get(key=token).user
        response.data.update(serializers.UserReadOnlySerializer(user).data)
        return response


class UserViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    filter_backends = [custom_filters.GenericFilterBackend, filters.SearchFilter]
    search_fields = ['^username', '^first_name', '^last_name']
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()

    def retrieve(self, request, *args, **kwargs):
        user = models.User.objects.get(id=kwargs['pk'])
        serializer = serializers.UserReadOnlySerializer(user)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        serializer = serializers.UserReadOnlySerializer(self.queryset, many=True)
        return Response(serializer.data)


class UpdateUserViewSet(mixins.UpdateModelMixin,
                        GenericViewSet):
    serializer_class = serializers.UpdateUserSerializer
    queryset = models.User.objects.all()


class TokenViewSet(mixins.RetrieveModelMixin,
                   GenericViewSet):
    serializer_class = serializers.TokenSerializer
    queryset = Token.objects.all()

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(self, request, *args, **kwargs)
        user = models.User.objects.get(id=response.data['user'])
        response.data['user'] = serializers.UserReadOnlySerializer(user).data
        return response


class AuthorViewSet(ModelViewSet):
    queryset = models.Author.objects.all()
    serializer_class = serializers.AuthorSerializer
    filter_backends = [custom_filters.GenericFilterBackend, filters.SearchFilter]
    search_fields = ['^user__username', '^user__first_name', '^user__last_name']


class NotificationViewSet(ModelViewSet):
    queryset = models.Notification.objects.all()
    serializer_class = serializers.NotificationSerializer
    filter_backends = [custom_filters.GenericFilterBackend]


class MCCViewSet(ModelViewSet):
    queryset = models.MCC.objects.all()
    serializer_class = serializers.MCCSerializer
    filter_backends = [custom_filters.GenericFilterBackend, filters.SearchFilter]
    search_fields = ['^id', '^area']


class ArticleViewSet(ModelViewSet):
    queryset = models.Article.objects.all()
    serializer_class = serializers.ArticleSerializer
    filter_backends = [custom_filters.GenericFilterBackend, filters.SearchFilter]
    search_fields = ['^title', '^keywords', '^author__user__username']

    def create(self, request, *args, **kwargs):
        result = super().create(request, args, kwargs)
        if result.status_code == 201:
            notification_maker.new_article(result.data['id'])
        return result

    def update(self, request, *args, **kwargs):
        previous_evaluation = models.Article.objects.get(id=kwargs['pk']).evaluation
        result = super().update(request, args, kwargs)
        if result.status_code == 200 and 'evaluation' in request.data:
            notification_maker.updated_article(result.data['id'], previous_evaluation)
        return result


class ParticipationViewSet(ModelViewSet):
    queryset = models.Participation.objects.all()
    serializer_class = serializers.ParticipationSerializer
    filter_backends = [custom_filters.GenericFilterBackend]

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = serializers.ParticipationReadOnlyFieldSerializer
        out = super().retrieve(request, *args, **kwargs)
        self.serializer_class = serializers.ParticipationSerializer
        return out

    def list(self, request, *args, **kwargs):
        self.serializer_class = serializers.ParticipationReadOnlyFieldSerializer
        out = super().list(request, *args, **kwargs)
        self.serializer_class = serializers.ParticipationSerializer
        return out

    def create(self, request, *args, **kwargs):
        result = super().create(request, args, kwargs)
        if result.status_code == 201:
            notification_maker.new_participation(result.data['id'])
        return result


class RefereeViewSet(ModelViewSet):
    queryset = models.Referee.objects.all()
    serializer_class = serializers.RefereeSerializer
    filter_backends = [custom_filters.GenericFilterBackend, filters.SearchFilter]
    search_fields = ['^user__username', '^user__first_name', '^user__last_name']


class ArticleInReviewViewSet(ModelViewSet):
    queryset = models.ArticleInReview.objects.all()
    serializer_class = serializers.ArticleInReviewSerializer
    filter_backends = [custom_filters.GenericFilterBackend]

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = serializers.ArticleInReviewReadOnlyFieldSerializer
        out = super().retrieve(request, *args, **kwargs)
        self.serializer_class = serializers.ArticleInReviewSerializer
        return out

    def list(self, request, *args, **kwargs):
        self.serializer_class = serializers.ArticleInReviewReadOnlyFieldSerializer
        out = super().list(request, *args, **kwargs)
        self.serializer_class = serializers.ArticleInReviewSerializer
        return out

    def create(self, request, *args, **kwargs):
        result = super().create(request, args, kwargs)
        if result.status_code == 201:
            notification_maker.new_review(result.data['id'])
        return result

    def update(self, request, *args, **kwargs):
        previous_state = models.ArticleInReview.objects.get(id=kwargs['pk']).state
        result = super().update(request, args, kwargs)
        if result.status_code == 200:
            notification_maker.updated_review(result.data['id'], previous_state)
        return result


class FileViewSet(ModelViewSet):
    queryset = models.File.objects.all()
    serializer_class = serializers.FileSerializer
    filter_backends = [custom_filters.GenericFilterBackend, filters.SearchFilter]
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


def download_report(request, pk: int) -> HttpResponse:
    id_notification = pk
    notification = models.Notification.objects.get(id=id_notification)
    author = models.Author.objects.get(user=notification.user)
    file_path = generate_document(str(author), author.institution, notification.content, notification.date)
    with open(file_path, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/msword")
        response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
        os.remove(file_path)
        return response
