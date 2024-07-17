from MainTree.models import UTNSubject
from rest_framework import viewsets, permissions
from .serializers import SubjectSerializer


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = UTNSubject.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = SubjectSerializer
    http_method_names = ['get']
