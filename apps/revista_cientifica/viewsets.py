import os

from django.conf import settings
from rest_framework import filters, mixins, status
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

import apps.revista_cientifica.models as models
import apps.revista_cientifica.serializers as serializers
from apps.revista_cientifica.tools import NotificationMaker, GenericFilterBackend

notification_maker = NotificationMaker()


class UserViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = models.User.objects.all().order_by('id')  # For avoid an UnorderedObjectListWarning
    filter_backends = [GenericFilterBackend, filters.SearchFilter]
    serializer_class = serializers.UserInfoSerializer
    search_fields = ['^username', '^first_name', '^last_name']


class UserCreateView(generics.CreateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer:serializers.UserCreateSerializer  = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # headers = self.get_success_headers(serializer.data)
        # return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        return Response(serializers.UserInfoSerializer(serializer.instance, many=False).data,
                        status=status.HTTP_201_CREATED)


class UserUpdateView(generics.UpdateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserUpdateSerializer

    def get_object(self):
        return self.queryset.get(id=self.kwargs['pk'])

    def update(self, request, *args, **kwargs):
        response = super(UserUpdateView, self).update(request, *args, **kwargs)

        if 400 <= response.status_code <= 599:  # error
            return response
        return Response(serializers.UserInfoSerializer(self.get_object()).data)


class UserRetrieveView(generics.RetrieveAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserInfoSerializer


class UserListView(generics.ListAPIView):
    queryset = models.User.objects.all().order_by('id')
    serializer_class = serializers.UserInfoSerializer
    filter_backends = [GenericFilterBackend, filters.SearchFilter]


class UserChangePasswordView(generics.UpdateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserChangePasswordSerializer

    def get_object(self):
        return self.queryset.get(id=self.kwargs['pk'])

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.update(instance, request.data)
        except ValueError:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({'new_password': serializer.data['new_password']})


class TokenViewSet(mixins.RetrieveModelMixin, GenericViewSet):
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
    filter_backends = [GenericFilterBackend]


class MCCViewSet(ModelViewSet):
    queryset = models.MCC.objects.all()
    serializer_class = serializers.MCCSerializer
    filter_backends = [GenericFilterBackend, filters.SearchFilter]
    search_fields = ['^id', '^area']


class ArticleViewSet(ModelViewSet):
    queryset = models.Article.objects.all()
    serializer_class = serializers.ArticleSerializer
    filter_backends = [GenericFilterBackend, filters.SearchFilter]
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
    filter_backends = [GenericFilterBackend]

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
    filter_backends = [GenericFilterBackend, filters.SearchFilter]
    search_fields = ['^user__username', '^user__first_name', '^user__last_name']


class ArticleInReviewViewSet(ModelViewSet):
    queryset = models.ArticleInReview.objects.all()
    serializer_class = serializers.ArticleInReviewSerializer
    filter_backends = [GenericFilterBackend]

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
    filter_backends = [GenericFilterBackend, filters.SearchFilter]
    search_fields = ['^file_name', '^article__title']

    def destroy(self, request, *args, **kwargs):
        file = models.File.objects.get(pk=kwargs['pk'])
        path = os.path.join(settings.BASE_DIR, file.file.name)
        os.remove(path)
        file.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        file = models.File.objects.get(pk=kwargs['pk'])
        path = os.path.join(settings.BASE_DIR, file.file.name)
        try:
            response = super().update(request, *args, **kwargs)
            os.remove(path)
            return response
        except Exception as e:
            raise e
