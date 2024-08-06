"""from .models import UTNSubject
from .subject_tree import SubjectTreeDB


def from_fathers_to_children():
    
    #Using the fathers array from every db subject, sets the children of the fathers
    
    subjects = list(UTNSubject.objects.all())
    for subject in subjects:
        if subject.regular_fathers == 'sistemas':
            continue

        fathers_array = SubjectTreeDB.parseStrList(subject.regular_fathers)
        for father in fathers_array:
            try:
                father_sql = UTNSubject.objects.get(id=father)
                if father_sql.regular_children == '':
                    father_sql.regular_children = str(subject.id)
                else:
                    father_sql.regular_children = father_sql.regular_children + \
                        str(f',{str(subject.id)}')

                father_sql.save()
            except Exception as e:
                print(e)
                continue
"""
