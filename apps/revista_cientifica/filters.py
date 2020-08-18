from rest_framework.filters import BaseFilterBackend
from django.db.models.query import QuerySet


class ParticipationFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset: QuerySet, view):
        try:
            if 'user__id' in request.query_params.keys():
                queryset = queryset.filter(author__user__id=request.query_params['user__id'])
            if 'user__email' in request.query_params.keys():
                queryset = queryset.filter(author__user__email=request.query_params['user__email'])
            if 'user__username' in request.query_params.keys():
                queryset = queryset.filter(author__user__username=request.query_params['user__username'])
            if 'author__id' in request.query_params.keys():
                queryset = queryset.filter(author__id=request.query_params['author__id'])
            if 'author__ORCID' in request.query_params.keys():
                queryset = queryset.filter(author__ORCID=request.query_params['author__ORCID'])
            if 'article__id' in request.query_params.keys():
                queryset = queryset.filter(article__id=request.query_params['article__id'])
            if 'article__title' in request.query_params.keys():
                queryset = queryset.filter(article__title=request.query_params['article__title'])
            if 'is_email_author' in request.query_params.keys():
                queryset = queryset.filter(is_email_author=request.query_params['is_email_author'])
        except Exception as e:
            queryset = queryset.none()
        return queryset


class ArticleInReviewFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset: QuerySet, view):
        try:
            if 'user__id' in request.query_params.keys():
                queryset = queryset.filter(referee__user__id=request.query_params['user__id'])
            if 'user__email' in request.query_params.keys():
                queryset = queryset.filter(referee__user__email=request.query_params['user__email'])
            if 'user__username' in request.query_params.keys():
                queryset = queryset.filter(referee__user__username=request.query_params['user__username'])
            if 'referee__id' in request.query_params.keys():
                queryset = queryset.filter(referee__id=request.query_params['referee__id'])
            if 'article__id' in request.query_params.keys():
                queryset = queryset.filter(article__id=request.query_params['article__id'])
            if 'article__title' in request.query_params.keys():
                queryset = queryset.filter(article__title=request.query_params['article__title'])
            if 'evaluation' in request.query_params.keys():
                queryset = queryset.filter(evaluation=request.query_params['evaluation'])
            if 'state' in request.query_params.keys():
                queryset = queryset.filter(state=request.query_params['state'])
            if 'round' in request.query_params.keys():
                queryset = queryset.filter(round=request.query_params['round'])
        except Exception as e:
            queryset = queryset.none()
        return queryset


class UserFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset: QuerySet, view):
        try:
            if 'id' in request.query_params.keys():
                queryset = queryset.filter(id=request.query_params['id'])
            if 'email' in request.query_params.keys():
                queryset = queryset.filter(email=request.query_params['email'])
            if 'username' in request.query_params.keys():
                queryset = queryset.filter(username=request.query_params['username'])
            if 'first_name' in request.query_params.keys():
                queryset = queryset.filter(first_name=request.query_params['first_name'])
            if 'last_name' in request.query_params.keys():
                queryset = queryset.filter(last_name=request.query_params['last_name'])
        except Exception as e:
            queryset = queryset.none()
        return queryset


class AuthorFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset: QuerySet, view):
        try:
            if 'id' in request.query_params.keys():
                queryset = queryset.filter(id=request.query_params['id'])
            if 'user__id' in request.query_params.keys():
                queryset = queryset.filter(user__id=request.query_params['user__id'])
            if 'user__email' in request.query_params.keys():
                queryset = queryset.filter(user__email=request.query_params['user__email'])
            if 'user__username' in request.query_params.keys():
                queryset = queryset.filter(user__username=request.query_params['user__username'])
            if 'ORCID' in request.query_params.keys():
                queryset = queryset.filter(ORCID=request.query_params['ORCID'])
            if 'intitution' in request.query_params.keys():
                queryset = queryset.filter(institution=request.query_params['institution'])
        except Exception as e:
            queryset = queryset.none()
        return queryset


class RefereeFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset: QuerySet, view):
        try:
            if 'user__id' in request.query_params.keys():
                queryset = queryset.filter(user__id=request.query_params['user__id'])
            if 'user__email' in request.query_params.keys():
                queryset = queryset.filter(user__email=request.query_params['user__email'])
            if 'user__username' in request.query_params.keys():
                queryset = queryset.filter(user__username=request.query_params['user__username'])
            if 'id' in request.query_params.keys():
                queryset = queryset.filter(id=request.query_params['id'])
        except Exception as e:
            queryset = queryset.none()
        return queryset


class GenericFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        dic = {}
        for item in request.query_params.keys():
            if item != 'many':
                dic[item] = request.query_params[item]
        many = True
        if 'many' in request.query_params.keys():
            many = request.query_params['many']
        try:
            if many:
                queryset = queryset.filter(**dic)
            else:
                queryset = queryset.get(**dic)
        except Exception as e:
            queryset = queryset.none()
        return queryset


