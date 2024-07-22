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

    """if request.method == 'POST':
        data = json.loads(request.body)
        action = data['action']
        # CUANDO SE QUIERA CONSULTAR SOLO LOS DATOS DE UN SUBJECT, RECURRIMOS A LA API REST QUE VAMOS A CREAR
        # CUANDO SE QUIERA CREAR TOD0 EL ARBOL Y PASARLO AL FRONT HACERLO DESDE LA VISTA EN BACKEND"""

    return render(request, 'index.html')
