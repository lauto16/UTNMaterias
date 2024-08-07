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

        fathers_array = SubjectTreeDB.parseStrList(subject.regular_fathers)
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
