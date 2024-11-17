# requests/forms.py
from django import forms
from django.utils import timezone
from .models import ServiceRequest, ServiceRequestType

class ServiceRequestForm(forms.ModelForm):
    request_type = forms.ModelChoiceField(
        queryset=ServiceRequestType.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )

    class Meta:
        model = ServiceRequest
        fields = ['request_type', 'description', 'scheduled_date']
        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Please describe your request...'
            }),
            'scheduled_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'},
                format='%Y-%m-%dT%H:%M'
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['scheduled_date'].input_formats = ['%Y-%m-%dT%H:%M']

class AttachmentForm(forms.Form):
    file = forms.FileField(label='Select a file')
