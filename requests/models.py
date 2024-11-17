# requests/models.py
from django import forms
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class ServiceRequestType(models.Model):
    CATEGORY_CHOICES = [
        ('billing', 'Billing Issue'),
        ('gas_leak', 'Gas Leak Emergency'),
        ('connection', 'New Connection'),
        ('maintenance', 'Maintenance'),
        ('meter', 'Meter Related'),
        ('other', 'Other Services')
    ]
    
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    is_emergency = models.BooleanField(default=False)
    estimated_completion_hours = models.PositiveIntegerField()
    requires_site_visit = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.get_category_display()} - {self.name}"

class ServiceRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('assigned', 'Assigned'),
        ('in_progress', 'In Progress'),
        ('on_hold', 'On Hold'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('priority', 'Priority')
    ]

    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    request_type = models.ForeignKey(ServiceRequestType, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    assigned_to = models.ForeignKey(
        User, 
        related_name='assigned_requests',
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL
    )
    scheduled_date = models.DateTimeField(null=True, blank=True)
    completed_date = models.DateTimeField(null=True, blank=True)
    internal_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Request #{self.id} - {self.customer.username}"

    def mark_completed(self):
        self.status = 'completed'
        self.completed_date = timezone.now()
        self.save()

class ServiceRequestAttachment(models.Model):
    service_request = models.ForeignKey(
        ServiceRequest,
        related_name='attachments',
        on_delete=models.CASCADE
    )
    file = models.FileField(upload_to='service_requests/')
    description = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attachment for Request #{self.service_request.id}"
    
    def clean_scheduled_date(self):
        scheduled_date = self.cleaned_data.get('scheduled_date')
        if scheduled_date and scheduled_date < timezone.now():
            raise forms.ValidationError("Scheduled date cannot be in the past")
        return scheduled_date