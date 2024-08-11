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


def add_fathers_final(career: str, final_id: int):
    model = SubjectViewSet.get_model_for_career(career)
    final = model.objects.get(id=final_id)
    subjects = list(model.objects.all())

    final_lista_fathers = SubjectTreeDB.parse_str_list(final.approval_fathers)

    for subject in subjects:
        if not (subject.id in final_lista_fathers) and subject.id != final_id:
            final.approval_fathers = final.approval_fathers + \
                str(f',{subject.id}')
    final.save()


def add_fathers_mid(career: str, mid_id: int):
    model = SubjectViewSet.get_model_for_career(career)
    mid = model.objects.get(id=mid_id)
    subjects = list(model.objects.all())

    mid_lista_fathers = SubjectTreeDB.parse_str_list(mid.approval_fathers)

    for subject in subjects:
        if not (subject.id in mid_lista_fathers) and subject.id != mid_id and subject.id < mid_id:
            mid.approval_fathers = mid.approval_fathers + \
                str(f',{subject.id}')
    mid.save()


def hijos(career: str, mid_id: int):
    model = SubjectViewSet.get_model_for_career(career)
    mid = model.objects.get(id=mid_id)
    subjects = [model.objects.get(
        id=id) for id in SubjectTreeDB.parse_str_list(mid.approval_fathers)]
    for subject in subjects:
        lista_hijos = SubjectTreeDB.parse_str_list(subject.approval_children)
        if not (mid_id in lista_hijos) and subject.id != mid_id:
            if lista_hijos:
                subject.approval_children = subject.approval_children + \
                    str(f',{mid_id}')
            else:
                subject.approval_children = mid_id

        subject.save()


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

    # agregar como padres de aprobacion a todos los anteriores al que se le pasa (titulo final)
    # add_fathers_final(career, 38)

    # agregar como padres de aprobacion a todos los anteriores al que se le pasa (titulo intermedio)
    # add_fathers_mid(career, 25)

    # agregar hijos de lo anterior
    # hijos(career, 38)

    return render(request, 'index.html', {'career': career})
