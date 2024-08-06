from django.shortcuts import render
from MainTree.subject_tree import *
from django.http import Http404


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

    return render(request, 'index.html', {'career': career})
