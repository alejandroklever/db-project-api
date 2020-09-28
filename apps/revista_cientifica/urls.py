from django.urls import path
from rest_framework import routers

import apps.revista_cientifica.viewsets as viewsets

router = routers.DefaultRouter()
router.register('author', viewsets.AuthorViewSet)
router.register('article', viewsets.ArticleViewSet)
router.register('notification', viewsets.NotificationViewSet)
router.register('file', viewsets.FileViewSet)
router.register('mcc', viewsets.MCCViewSet)
router.register('participation', viewsets.ParticipationViewSet)
router.register('referee', viewsets.RefereeViewSet)
router.register('article_in_review', viewsets.ArticleInReviewViewSet)
router.register('token', viewsets.TokenViewSet, basename='token')
router.register('user', viewsets.UserViewSet, basename='user')


urlpatterns = (
    router.urls + [
        path('auth/', viewsets.UserAuthView.as_view()),
    ]
)
