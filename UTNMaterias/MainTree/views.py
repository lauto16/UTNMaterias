from django.shortcuts import render
from MainTree.subject_tree import *


def index(request):
    db_tree = SubjectTreeDB(career='sistemas', tree_type='approval')
    print(db_tree.tree)
    return render(request, 'index.html')
