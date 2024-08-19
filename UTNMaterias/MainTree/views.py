from django.views.decorators.csrf import ensure_csrf_cookie
from json import loads as json_loads
from django.shortcuts import render
from django.http import Http404


@ensure_csrf_cookie
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
        data = json_loads(request.body)
        action = data['action']

    return render(request, 'index.html', {'career': career})
