from rest_framework import routers

from .viewsets import (UserViewSet, AuthorViewSet, ArticleViewSet, NotificationViewSet, FileViewSet, MCCViewSet,
                       ParticipationViewSet, RefereeViewSet)

router = routers.SimpleRouter()
router.register('user', UserViewSet)
router.register('author', AuthorViewSet)
router.register('article', ArticleViewSet)
router.register('notification', NotificationViewSet)
router.register('file', FileViewSet)
router.register('mcc', MCCViewSet)
router.register('participation', ParticipationViewSet)
router.register('referee', RefereeViewSet)
router.register('article_in_review', ArticleViewSet)

urlpatterns = router.urls
