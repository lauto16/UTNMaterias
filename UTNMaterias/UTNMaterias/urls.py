from django.contrib import admin
from django.urls import path, include
from MainTree.views import *
from Selector.views import *
from SubjectAPI.urls import *
from TreeAPI.urls import *

# modificar el url de la api de subject para pedir la carrera tambien
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', selector_view, name='selector'),
    path('index/<str:career>', index, name='index'),
    path('subject_api/', include('SubjectAPI.urls')),
    path('tree_api/', include('TreeAPI.urls'))
]
