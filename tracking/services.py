# tracking/services.py
from django.db import transaction
from .models import RequestStatus, Notification

class TrackingService:
    @staticmethod
    @transaction.atomic
    def create_status_update(service_request, new_status, notes, user):
        """
        Create a status update and notify relevant users
        """
        # Create status update
        status_update = RequestStatus.objects.create(
            service_request=service_request,
            status=new_status,
            notes=notes,
            created_by=user
        )
        
        # Create notification for customer
        Notification.objects.create(
            user=service_request.customer,
            service_request=service_request,
            notification_type='status_update',
            message=f'Your request status has been updated to {new_status}'
        )
        
        # If request is assigned, notify staff member
        if new_status == 'assigned' and service_request.assigned_to:
            Notification.objects.create(
                user=service_request.assigned_to,
                service_request=service_request,
                notification_type='assignment',
                message=f'You have been assigned to request #{service_request.id}'
            )
        
        return status_update