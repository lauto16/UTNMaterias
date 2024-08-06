from MainTree.models import *
from rest_framework import viewsets, permissions
from .serializers import SubjectSerializer
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.shortcuts import render


class SubjectViewSet(viewsets.ModelViewSet):
    """
    API Used to return subject's data when passing a career and id as url argument.
    It only lets the user do 'get' requests.
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = SubjectSerializer
    http_method_names = ['get']

    def get_queryset(self):
        career = self.kwargs.get('career')
        subject_id = self.kwargs.get('id')

        model = self.get_model_for_career(career)
        if model is None:
            return Response({"detail": "Career not found."}, status=404)

        queryset = model.objects.filter(id=subject_id)

        return queryset

    def get_model_for_career(self, career):
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
