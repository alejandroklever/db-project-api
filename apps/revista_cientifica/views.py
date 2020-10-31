import os

from django.conf import settings
from django.http import HttpResponse, Http404
from rest_framework import generics, status, filters
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

from apps.revista_cientifica import models, serializers
from apps.revista_cientifica.tools import GenericFilterBackend
from apps.revista_cientifica.tools.documents import generate_document


class UserRetrieveView(generics.RetrieveAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserInfoSerializer


class UserListView(generics.ListAPIView):
    queryset = models.User.objects.all().order_by('id')
    serializer_class = serializers.UserInfoSerializer
    filter_backends = [GenericFilterBackend, filters.SearchFilter]


class UserCreateView(generics.CreateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        response_data = serializers.UserInfoSerializer(serializer.instance).data
        response_data['token'] = Token.objects.get(user_id=response_data['id']).key

        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)


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


class UserAuthView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(UserAuthView, self).post(request, *args, **kwargs)
        token = response.data['token']
        user = Token.objects.get(key=token).user
        response.data.update(serializers.UserInfoSerializer(user).data)
        return response


def download_file(request, path: str):
    file_path = os.path.join(settings.BASE_DIR, 'apps', 'revista_cientifica', 'media', path)
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


class CoAuthorsListView(generics.RetrieveAPIView):
    queryset = models.Participation.objects.all().order_by('id')
    serializer_class = None
    filter_backends = [GenericFilterBackend, filters.SearchFilter]

    def retrieve(self, request, *args, **kwargs):
        author = models.Author.objects.get(id=kwargs['pk'])
        participations = models.Participation.objects.filter(author=author)
        articles = [participation.article for participation in participations]
        authors_par = [models.Participation.objects.filter(article=article) for article in articles]
        authors = [[par.author for par in parts] for parts in authors_par]
        files = [models.File.objects.filter(article=article).order_by('id') for article in articles]
        files = [item[-1] if len(item) > 0 else None for item in files]
        data = []
        for article, author, file in zip(articles, authors, files):
            data.append({
                'article': serializers.ArticleSerializer(article).data,
                'authors': [serializers.UserInfoSerializer(item.user).data for item in author],
                'file': f'{file.file.name if file is not None else None}'
            })
        return Response({'data': data})
