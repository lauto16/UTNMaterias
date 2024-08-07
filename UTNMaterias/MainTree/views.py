from django.shortcuts import render
from MainTree.subject_tree import *
from django.http import Http404
import json

from .models import *
from .subject_tree import SubjectTreeDB
from SubjectAPI.api import SubjectViewSet


def from_fathers_to_children(career: str):

    # Using the fathers array from every db subject, sets the children of the fathers
    model = SubjectViewSet.get_model_for_career(career)
    subjects = list(model.objects.all())
    for subject in subjects:
        if subject.regular_fathers == career:
            continue

        fathers_array = SubjectTreeDB.parse_str_list(subject.regular_fathers)
        for father in fathers_array:
            try:
                father_sql = model.objects.get(id=father)
                if father_sql.regular_children == '':
                    father_sql.regular_children = str(subject.id)
                else:
                    father_sql.regular_children = father_sql.regular_children + \
                        str(f',{str(subject.id)}')

                father_sql.save()
            except Exception as e:
                print(e)
                continue

    for subject in subjects:
        if subject.approval_fathers == career:
            continue

        fathers_array = SubjectTreeDB.parse_str_list(subject.approval_fathers)
        for father in fathers_array:
            try:
                father_sql = model.objects.get(id=father)
                if father_sql.approval_children == '':
                    father_sql.approval_children = str(subject.id)
                else:
                    father_sql.approval_children = father_sql.approval_children + \
                        str(f',{str(subject.id)}')

                father_sql.save()
            except Exception as e:
                print(e)
                continue


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

    if request.method == 'POST':
        data = json.loads(request.body)
        action = data['action']

    # descomentar solo para agregar childrens a fathers en a bd
    # from_fathers_to_children(career)

    return render(request, 'index.html', {'career': career})
