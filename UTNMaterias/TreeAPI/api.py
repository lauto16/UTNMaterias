from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from MainTree.subject_tree import SubjectTreeDB


class TreeViewSet(viewsets.ModelViewSet):
    """
    API that returns a SubjectTree from a given career:
    (sistemas,metalurgica,mecanica,quimica,industrial,electrica,electronica,civil) 

    Returns:
        Response: An http response
    """

    permission_classes = [permissions.AllowAny]
    http_method_names = ['get']

    @action(detail=False, methods=['get'], url_path='career/(?P<career>[^/.]+)')
    def get_tree(self, request, career=None):
        if career:
            subject_tree = SubjectTreeDB(
                career=career, tree_type='approval').as_dict()
            return Response(subject_tree)
        return Response({"error": "Career not specified"}, status=400)
