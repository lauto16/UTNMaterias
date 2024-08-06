from rest_framework import routers
from .api import SubjectViewSet

# aca deberia haber otra division en el url que sea para la carrera, ya que cada carrera tiene su model
router = routers.DefaultRouter()
router.register(
    r'subjects/(?P<career>[^/.]+)/(?P<id>\d+)', SubjectViewSet, 'subjects')

urlpatterns = router.urls
