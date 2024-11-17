# staff/services.py
from django.db import transaction
from requests.models import ServiceRequest
from tracking.services import TrackingService

class StaffService:
    @staticmethod
    @transaction.atomic
    def assign_request(request_id, staff_user, notes=None):
        """
        Assign a service request to a staff member
        """
        service_request = ServiceRequest.objects.get(pk=request_id)
        service_request.assigned_to = staff_user
        service_request.status = 'assigned'
        service_request.save()
        
        # Create status update and notifications
        TrackingService.create_status_update(
            service_request=service_request,
            new_status='assigned',
            notes=notes,
            user=staff_user
        )
        
        return service_request

    @staticmethod
    @transaction.atomic
    def mark_priority(request_id, staff_user, notes=None):
        """
        Mark a service request as priority
        """
        service_request = ServiceRequest.objects.get(pk=request_id)
        service_request.status = 'priority'
        service_request.save()
        
        # Create status update and notifications
        TrackingService.create_status_update(
            service_request=service_request,
            new_status='priority',
            notes=notes,
            user=staff_user
        )
        
        return service_request