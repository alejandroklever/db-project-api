from django.urls import path
from rest_framework import routers

from apps.revista_cientifica import views, viewsets

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

urlpatterns = (
    router.urls + [
        path('auth/', views.UserAuthView.as_view()),
        path('user/', views.UserListView.as_view()),
        path('user/<int:pk>/', views.UserRetrieveView.as_view()),
        path('user/create/', views.UserCreateView.as_view()),
        path('user/update/<int:pk>/', views.UserUpdateView.as_view()),
        path('user/change_password/<int:pk>/', views.UserChangePasswordView.as_view())
    ]
)
