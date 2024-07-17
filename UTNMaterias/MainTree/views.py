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

        if action == 'getSubject':
            subject_sql_id = int(data['subject_id'])

            try:
                # subject_data = db_tree.tree.search(
                # sql_id=subject_sql_id, actual_subject=db_tree.tree.root).as_dict()

                print(db_tree.tree.root)

                return JsonResponse({'success': True, 'subject': 'subject_data'})

            except Exception as e:
                print(e)
                return JsonResponse(
                    {
                        'success': False
                    }
                )
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
