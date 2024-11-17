from django import forms
from django.utils import timezone

from requests.models import ServiceRequestType
from .models import Notification, RequestStatus, SLATracking

class StatusUpdateForm(forms.ModelForm):
    """Form for updating request status with notes"""
    
    notes = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 3,
            'class': 'form-control',
            'placeholder': 'Add notes about this status update...'
        }),
        required=False
    )
    
    internal_notes = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 3,
            'class': 'form-control',
            'placeholder': 'Add internal notes (not visible to customer)...'
        }),
        required=False
    )

    class Meta:
        model = RequestStatus
        fields = ['status', 'notes', 'internal_notes']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].widget.attrs.update({'class': 'form-control'})

class SLATrackingForm(forms.ModelForm):
    """Form for managing SLA tracking"""
    
    sla_target = forms.DurationField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., 24:00:00 for 24 hours'
        })
    )
    
    sla_deadline = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control'
        })
    )

    class Meta:
        model = SLATracking
        fields = ['sla_target', 'sla_deadline']

    def clean_sla_deadline(self):
        deadline = self.cleaned_data.get('sla_deadline')
        if deadline and deadline < timezone.now():
            raise forms.ValidationError("SLA deadline cannot be in the past")
        return deadline

class NotificationFilterForm(forms.Form):
    """Form for filtering notifications"""
    
    NOTIFICATION_TYPES = [('', 'All Types')] + Notification.NOTIFICATION_TYPES
    
    notification_type = forms.ChoiceField(
        choices=NOTIFICATION_TYPES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )
    
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )
    
    read_status = forms.ChoiceField(
        choices=[
            ('', 'All'),
            ('unread', 'Unread'),
            ('read', 'Read')
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class MetricsFilterForm(forms.Form):
    """Form for filtering metrics data"""
    
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )
    
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )
    
    request_type = forms.ModelChoiceField(
        queryset=ServiceRequestType.objects.all(),
        required=False,
        empty_label="All Types",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    include_sla_breached = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError("Start date must be before end date")
        
        return cleaned_data