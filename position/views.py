from re import search

from django.db.models import Count
from django.db.models.expressions import result
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Lead, ActionHistory
from .serializers import LeadSerializer, LeadStatusUpdateSerializer, List_amar_serializer
from django.db import transaction
from rest_framework import status


# Create your views here.


class LeadListAPIView(APIView):
    def get(self, request):
        search = request.query_params.get('search')
        if search:
            leads = Lead.objects.filter(source__contains=search)
        else:
            leads = Lead.objects.all()

        serializer = LeadSerializer(leads, many=True)
        print(search)
        return Response(serializer.data)


class LeadStatusUpdateAPIView(APIView):
    def post(self, request, lead_id):
        try:
            lead = Lead.objects.get(id=lead_id)
        except Lead.DoesNotExist:
            return Response(
                {"detail": "Lead not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = LeadStatusUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_status = serializer.validated_data['status']
        old_status = lead.status

        if old_status == new_status:
            return Response(
                {"detail": "Status is already the same"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 🔥 Transaction starts here
        with transaction.atomic():
            lead.status = new_status
            lead.save()

            ActionHistory.objects.create(
                lead=lead,
                from_status=old_status,
                to_status=new_status
            )

        return Response(
            {"detail": "Status updated successfully"},
            status=status.HTTP_200_OK
        )

class Lead_list(APIView):
    def get(self, request):
        result = Lead.objects.values('status').annotate(
            status_count=Count('status')
        ).order_by('-status_count')
        serializer = List_amar_serializer(result, many=True)

        return Response(serializer.data)