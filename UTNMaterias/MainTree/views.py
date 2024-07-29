from MainTree.models import UTNSubject
from MainTree.subject_tree import ApprovalSubject
from rest_framework.views import APIView
from django.shortcuts import render
from MainTree.subject_tree import *
from django.http import JsonResponse, Http404
import requests
from random import choice


def index(request, career: str):
    careers = [
        'civil',
        'electrica',
        'electronica',
        'industrial',
        'mecanica',
        'metalurgica',
        'quimica',
        'sistemas'
    ]

    if not (career in careers):
        raise Http404("La carrera seleccionada no existe.")

    db_tree = SubjectTreeDB(career=career, tree_type='approval')
    print(db_tree.tree)

    if request.method == 'POST':
        data = json.loads(request.body)
        action = data['action']

        if action == 'get_tree':
            """
            la forma de enviar el arbol sera mediante JsonResponse({
                'success': Bool,

                'materia1': {
                        id: 1,
                        name: 'Analisis matematico',
                        children: [2,3,5]
                },
                'materia2': {
                        id: 2,
                        name: 'Fisica',
                        children: [3,5]
                },
            })

            """
            return JsonResponse({'success': True})

    return render(request, 'index.html')
