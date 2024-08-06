from MainTree.models import UTNSubjectSistemas
from rest_framework import viewsets, permissions
from .serializers import SubjectSerializer


class SubjectViewSet(viewsets.ModelViewSet):
    """
    API Used to return subject's data when passing an id as url argument.
    It only let the user do 'get' requests.  
    """

    # aca tiene que haber un selector que elija la clase model de esa carrera
    queryset = UTNSubjectSistemas.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = SubjectSerializer
    http_method_names = ['get']
