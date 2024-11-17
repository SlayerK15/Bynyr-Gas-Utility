# requests/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import ServiceRequest, ServiceRequestAttachment, ServiceRequestType
from .forms import ServiceRequestForm, AttachmentForm
from .serializers import ServiceRequestSerializer
from django.utils.dateparse import parse_datetime

@login_required
def create_request(request):
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST)
        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.customer = request.user
            service_request.save()
            messages.success(request, 'Request created successfully!')
            return redirect('requests:request_detail', pk=service_request.pk)
        else:
            print(form.errors)  # Debugging: Print form errors to console
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ServiceRequestForm()

    return render(request, 'requests/create_request.html', {'form': form})

@login_required
def request_detail(request, pk):
    service_request = get_object_or_404(ServiceRequest, pk=pk)
    if not request.user.is_staff and request.user != service_request.customer:
        messages.error(request, "You don't have permission to view this request.")
        return redirect('accounts:customer_dashboard')
    
    return render(request, 'requests/request_detail.html', {
        'request': service_request
    })

@login_required
def request_list(request):
    if request.user.is_staff:
        requests = ServiceRequest.objects.all()
    else:
        requests = ServiceRequest.objects.filter(customer=request.user)
    
    requests = requests.select_related('customer', 'request_type').order_by('-created_at')
    
    return render(request, 'requests/request_list.html', {
        'requests': requests
    })

@login_required
def update_request(request, pk):
    service_request = get_object_or_404(ServiceRequest, pk=pk)
    
    # Check permissions
    if not request.user.is_staff and request.user != service_request.customer:
        messages.error(request, "You don't have permission to update this request.")
        return redirect('accounts:customer_dashboard')
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        notes = request.POST.get('notes')
        
        if new_status:
            old_status = service_request.status
            service_request.status = new_status
            
            if new_status == 'completed':
                service_request.completed_date = timezone.now()
            
            service_request.save()
            
            # Add status change to internal notes if provided
            if notes:
                if service_request.internal_notes:
                    service_request.internal_notes += f"\n[{timezone.now()}] Status changed from {old_status} to {new_status}: {notes}"
                else:
                    service_request.internal_notes = f"[{timezone.now()}] Status changed from {old_status} to {new_status}: {notes}"
                service_request.save()
            
            messages.success(request, 'Request updated successfully')
            return redirect('requests:request_detail', pk=pk)
    
    context = {
        'service_request': service_request,
        'status_choices': ServiceRequest.STATUS_CHOICES,
    }
    return render(request, 'requests/update_request.html', context)

@login_required
def cancel_request(request, pk):
    service_request = get_object_or_404(ServiceRequest, pk=pk)
    
    # Check permissions
    if not request.user.is_staff and request.user != service_request.customer:
        messages.error(request, "You don't have permission to cancel this request.")
        return redirect('accounts:customer_dashboard')
    
    if request.method == 'POST':
        notes = request.POST.get('notes', '')
        service_request.status = 'cancelled'
        
        if notes:
            if service_request.internal_notes:
                service_request.internal_notes += f"\n[{timezone.now()}] Request cancelled: {notes}"
            else:
                service_request.internal_notes = f"[{timezone.now()}] Request cancelled: {notes}"
        
        service_request.save()
        messages.success(request, 'Request cancelled successfully')
        return redirect('requests:request_list')
    
    return render(request, 'requests/cancel_request.html', {
        'service_request': service_request
    })

@login_required
def add_attachment(request, pk):
    service_request = get_object_or_404(ServiceRequest, pk=pk)
    
    # Check permissions
    if not request.user.is_staff and request.user != service_request.customer:
        messages.error(request, "You don't have permission to add attachments.")
        return redirect('accounts:customer_dashboard')
    
    if request.method == 'POST':
        files = request.FILES.getlist('attachments')
        
        for f in files:
            ServiceRequestAttachment.objects.create(
                service_request=service_request,
                file=f
            )
        
        messages.success(request, 'Attachments added successfully')
        return redirect('requests:request_detail', pk=pk)
    
    return render(request, 'requests/add_attachment.html', {
        'service_request': service_request
    })