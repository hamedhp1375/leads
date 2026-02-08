from django.urls import path
from .views import LeadListAPIView, Lead_list
from .views import LeadStatusUpdateAPIView
urlpatterns = [
    path('leads/', LeadListAPIView.as_view(), name='lead-list'),
    path(
        'leads/<int:lead_id>/status/',
        LeadStatusUpdateAPIView.as_view(),
        name='lead-status-update'
    ),
    path("armar/", Lead_list.as_view(), name='lead-amar'),
]
