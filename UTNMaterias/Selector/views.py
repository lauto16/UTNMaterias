from django.shortcuts import render
from MainTree.views import index
from django.http import JsonResponse
import json


def selector_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        career = data['career']
        return JsonResponse({'career': career})

    return render(request, 'selector.html')
