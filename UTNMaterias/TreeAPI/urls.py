from rest_framework import routers
from .api import TreeViewSet


router = routers.DefaultRouter()
router.register('tree', TreeViewSet, basename='tree')

urlpatterns = router.urls
