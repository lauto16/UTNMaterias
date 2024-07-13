from django.contrib import admin
from django.urls import path
from MainTree.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index')
]
