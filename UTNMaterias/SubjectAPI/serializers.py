from rest_framework import serializers
from MainTree.models import UTNSubjectSistemas


class SubjectSerializer(serializers.ModelSerializer):
    """
    Serializes JSON to Model and vice versa
    """
    class Meta:
        model = UTNSubjectSistemas
        fields = ('id', 'name', 'approval_fathers',
                  'approval_children', 'regular_fathers', 'regular_children')
        read_only_fields = ('id', 'name', 'approval_fathers',
                            'approval_children', 'regular_fathers', 'regular_children')
