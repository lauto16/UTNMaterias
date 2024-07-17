from rest_framework import routers
from .api import SubjectViewSet

router = routers.DefaultRouter()
router.register('subjects', SubjectViewSet, 'subjects')

urlpatterns = router.urls
