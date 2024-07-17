from django.shortcuts import render
from MainTree.subject_tree import *
from django.http import JsonResponse
import requests


def index(request):
    # combine trees
    db_tree = SubjectTreeDB(career='sistemas', tree_type='approval')
    print(db_tree.tree)

    if request.method == 'POST':
        data = json.loads(request.body)
        action = data['action']

        # CUANDO SE QUIERA CONSULTAR SOLO LOS DATOS DE UN SUBJECT, RECURRIMOS A LA API REST QUE VAMOS A CREAR
        # CUANDO SE QUIERA CREAR TOD0 EL ARBOL Y PASARLO AL FRONT HACERLO DESDE LA VISTA EN BACKEND

    return render(request, 'index.html')

    """

from MainTree.models import UTNSubject
from django.http import JsonResponse
from rest_framework.views import APIView
from MainTree.subject_tree import ApprovalSubject


class SubjectsAPIView(APIView):
    REST API that returns subject data and its fathers data

    def get_subject_data(subject_id):

        Returns all the data for a certain subject

        Args:
            subject_id (_type_): _description_
        pass

    def get(self, request, subject_id, subject_type):

        # VER COMO HACER 
        if subject_type == 'approval':
            try:
                subject = UTNSubject.objects.get(id=subject_id)
                approval_subject = ApprovalSubject(
                    is_approved=False, sql_id=subject.id, name=subject.name, is_enrollable=False)

                return JsonResponse(approval_subject.as_dict())

            except UTNSubject.DoesNotExist:
                return JsonResponse({"error": "Subject doesn't exist"})

        elif subject_type == 'regular':
            pass

    
    """
