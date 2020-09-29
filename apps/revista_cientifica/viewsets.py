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
        response.data.update(serializers.UserInfoSerializer(user).data)
        return response


class UserViewSet(ModelViewSet):
    queryset = models.User.objects.all()
    filter_backends = [custom_filters.GenericFilterBackend, filters.SearchFilter]
    serializer_class = serializers.UserCreateSerializer

    info_serializer_class = serializers.UserInfoSerializer
    create_serializer_class = serializers.UserCreateSerializer
    update_serializer_class = serializers.UserUpdateSerializer
    search_fields = ['^username', '^first_name', '^last_name']

    def create(self, request, *args, **kwargs):
        self.serializer_class = self.create_serializer_class
        response = super(UserViewSet, self).create(request, *args, **kwargs)

        if 400 <= response.status_code <= 599:  # error
            return response
        return Response(self.info_serializer_class(self.get_object()).data)

    def update(self, request, *args, **kwargs):
        self.serializer_class = self.update_serializer_class
        response = super(UserViewSet, self).update(request, *args, **kwargs)

        if 400 <= response.status_code <= 599:  # error
            return response
        return Response(self.info_serializer_class(self.get_object()).data)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = self.info_serializer_class
        response = super(UserViewSet, self).retrieve(request, *args, **kwargs)
        return response

    def list(self, request, *args, **kwargs):
        self.serializer_class = self.info_serializer_class
        response = super(UserViewSet, self).list(request, *args, **kwargs)
        self.serializer_class = self.create_serializer_class
        return response


class TokenViewSet(mixins.RetrieveModelMixin,
                   GenericViewSet):
    serializer_class = serializers.TokenSerializer
    queryset = Token.objects.all()

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(self, request, *args, **kwargs)
        user = models.User.objects.get(id=response.data['user'])
        response.data['user'] = serializers.UserInfoSerializer(user).data
        return response


class AuthorViewSet(ModelViewSet):
    queryset = models.Author.objects.all()
    serializer_class = serializers.AuthorSerializer


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
        response = super(ParticipationViewSet, self).retrieve(request, *args, **kwargs)
        self.serializer_class = serializers.ParticipationSerializer
        return response

    def list(self, request, *args, **kwargs):
        self.serializer_class = serializers.ParticipationReadOnlyFieldSerializer
        response = super(ParticipationViewSet, self).list(request, *args, **kwargs)
        self.serializer_class = serializers.ParticipationSerializer
        return response

    def create(self, request, *args, **kwargs):
        result = super(ParticipationViewSet, self).create(request, args, kwargs)
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

    default_serializer_class = serializers.ArticleInReviewSerializer
    info_serializer_class = serializers.ArticleInReviewInfoSerializer

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = serializers.ArticleInReviewInfoSerializer
        response = super(ArticleInReviewViewSet, self).retrieve(request, *args, **kwargs)
        self.serializer_class = serializers.ArticleInReviewSerializer
        return response

    def list(self, request, *args, **kwargs):
        self.serializer_class = serializers.ArticleInReviewInfoSerializer
        response = super(ArticleInReviewViewSet, self).list(request, *args, **kwargs)
        self.serializer_class = serializers.ArticleInReviewSerializer
        return response

    def create(self, request, *args, **kwargs):
        response = super(ArticleInReviewViewSet, self).create(request, args, kwargs)

        if response.status_code == 201:
            notification_maker.new_review(response.data['id'])
        return response

    def update(self, request, *args, **kwargs):
        previous_state = models.ArticleInReview.objects.get(id=kwargs['pk']).state
        response = super(ArticleInReviewViewSet, self).update(request, args, kwargs)

        if response.status_code == 200:
            notification_maker.updated_review(response.data['id'], previous_state)
        return response


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



