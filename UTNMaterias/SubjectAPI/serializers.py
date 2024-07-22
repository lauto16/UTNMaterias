from rest_framework import serializers
from MainTree.models import UTNSubject


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = UTNSubject
        fields = ('id', 'name', 'approval_fathers',
                  'approval_children', 'regular_fathers', 'regular_children')
        read_only_fields = ('id', 'name', 'approval_fathers',
                            'approval_children', 'regular_fathers', 'regular_children')