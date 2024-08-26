from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
import json


@ensure_csrf_cookie
def selector_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        career = data['career']
        return JsonResponse({'career': career})
    return render(request, 'selector.html')


def login_view(request):
    return render(request, 'login.html')
