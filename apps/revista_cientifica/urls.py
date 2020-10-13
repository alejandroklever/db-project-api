from django.urls import path
from rest_framework import routers

import apps.revista_cientifica.viewsets as viewsets
from apps.revista_cientifica.views import UserAuthView

router = routers.DefaultRouter()
router.register('author', viewsets.AuthorViewSet)
router.register('article', viewsets.ArticleViewSet)
router.register('notification', viewsets.NotificationViewSet)
router.register('file', viewsets.FileViewSet)
router.register('mcc', viewsets.MCCViewSet)
router.register('participation', viewsets.ParticipationViewSet)
router.register('referee', viewsets.RefereeViewSet)
router.register('article_in_review', viewsets.ArticleInReviewViewSet)
router.register('token', viewsets.TokenViewSet)
# router.register('user', viewsets.UserViewSet)

urlpatterns = (
    router.urls + [
        path('auth/', UserAuthView.as_view()),
        path('user/', viewsets.UserListView.as_view()),
        path('user/<int:pk>/', viewsets.UserRetrieveView.as_view()),
        path('user/create/', viewsets.UserCreateView.as_view()),
        path('user/update/<int:pk>/', viewsets.UserUpdateView.as_view()),
        path('user/change_password/<int:pk>/', viewsets.UserChangePasswordView.as_view())
    ]
)
