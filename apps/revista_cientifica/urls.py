from django.urls import path
from rest_framework import routers

from .viewsets import (UserViewSet, DetailUserViewSet, UpdateUserViewSet, AuthorViewSet,
                       ArticleViewSet, NotificationViewSet, FileViewSet, MCCViewSet,
                       ParticipationViewSet, RefereeViewSet)

router = routers.DefaultRouter()
router.register('author', AuthorViewSet)
router.register('article', ArticleViewSet)
router.register('notification', NotificationViewSet)
router.register('file', FileViewSet)
router.register('mcc', MCCViewSet)
router.register('participation', ParticipationViewSet)
router.register('referee', RefereeViewSet)
router.register('article_in_review', ArticleViewSet)
router.register('user', UserViewSet, basename='user')
router.register('user', DetailUserViewSet, basename='user')
router.register('user/update', UpdateUserViewSet, basename='update user')

urlpatterns = (
    router.urls + [
    ]
)
