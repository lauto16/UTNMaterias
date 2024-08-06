from django.shortcuts import render
from django.http import JsonResponse
import json


def selector_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        career = data['career']
        return JsonResponse({'career': career})

    return render(request, 'selector.html')
