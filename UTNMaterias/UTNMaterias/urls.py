from django.contrib import admin
from django.urls import path, include
from MainTree.views import *
from Selector.views import *
from SubjectAPI.urls import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', selector_view, name='selector'),
    path('index/<str:career>', index, name='index'),
    path('apis/', include('SubjectAPI.urls'))
]
