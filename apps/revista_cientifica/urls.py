from rest_framework import routers

from .viewsets import UserViewSet

router = routers.SimpleRouter()
router.register('user', UserViewSet)

urlpatterns = router.urls
