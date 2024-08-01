from MainTree.models import UTNSubject
from rest_framework import viewsets, permissions
from .serializers import SubjectSerializer


class SubjectViewSet(viewsets.ModelViewSet):
    """
    API Used to return subject's data when passing an id as url argument.
    It only let the user do 'get' requests.  
    """
    queryset = UTNSubject.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = SubjectSerializer
    http_method_names = ['get']
