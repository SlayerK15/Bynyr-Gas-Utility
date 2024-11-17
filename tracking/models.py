# tracking/models.py
from django.db import models
from django.contrib.auth.models import User
from requests.models import ServiceRequest

class RequestStatus(models.Model):
    service_request = models.ForeignKey(
        ServiceRequest,
        related_name='status_updates',
        on_delete=models.CASCADE
    )
    status = models.CharField(max_length=20, choices=ServiceRequest.STATUS_CHOICES)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Request statuses'

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('status_update', 'Status Update'),
        ('assignment', 'Request Assignment'),
        ('comment', 'New Comment'),
        ('priority', 'Priority Change')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service_request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    message = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
