from django.contrib import admin
from django.urls import path, include
from MainTree.views import *
from SubjectAPI.urls import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('apis/', include('SubjectAPI.urls'))
]
