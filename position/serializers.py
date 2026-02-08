from rest_framework import serializers
from .models import Lead


class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = [
            'id',
            'name',
            'phone',
            'email',
            'source',
            'status',
            'created',
        ]


class LeadStatusUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(
        choices=Lead.status_choices
    )


class List_amar_serializer(serializers.Serializer):
    status = serializers.CharField()
    total = serializers.IntegerField(source="status_count")
