# tracking/serializers.py
from rest_framework import serializers
from .models import RequestStatus, Notification

class RequestStatusSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = RequestStatus
        fields = ('id', 'service_request', 'status', 'status_display',
                 'notes', 'created_by', 'created_by_name', 'created_at')

class NotificationSerializer(serializers.ModelSerializer):
    request_number = serializers.CharField(
        source='service_request.id',
        read_only=True
    )
    
    class Meta:
        model = Notification
        fields = ('id', 'user', 'service_request', 'request_number',
                 'notification_type', 'message', 'read', 'created_at')