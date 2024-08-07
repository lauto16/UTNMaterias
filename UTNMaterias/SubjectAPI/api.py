from MainTree.models import *
from rest_framework import viewsets, permissions
from .serializers import SubjectSerializer
from rest_framework.response import Response


class SubjectViewSet(viewsets.ModelViewSet):
    """
    API Used to return subject's data when passing a career and id as url argument.
    It only lets the user do 'get' requests.
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = SubjectSerializer
    http_method_names = ['get']

    def get_queryset(self):
        """
        Returns the subject whose id = subject_id (url argument)

        Returns:
            queryset: Contains all the matches 
        """
        career = self.kwargs.get('career')
        subject_id = self.kwargs.get('id')

        model = self.get_model_for_career(career)
        if model is None:
            return Response({"detail": "Career not found."}, status=404)

        queryset = model.objects.filter(id=subject_id)

        return queryset

    @staticmethod
    def get_model_for_career(career: str):
        """
        Returns the UTNSubject model class of a given career

        Args:
            career (str): An UTN career, must be: civil, electrica, electronica, industrial, mecanica, metalurgica, quimica or sistemas

        Returns:
            UTNSubject: UTNSubject model class
        """
        career_model_map = {
            'civil': UTNSubjectCivil,
            'electrica': UTNSubjectElectrica,
            'electronica': UTNSubjectElectronica,
            'industrial': UTNSubjectIndustrial,
            'mecanica': UTNSubjectMecanica,
            'metalurgica': UTNSubjectMetalurgica,
            'quimica': UTNSubjectQuimica,
            'sistemas': UTNSubjectSistemas
        }

        # Returns None if career doesn't exist
        return career_model_map.get(career, None)
