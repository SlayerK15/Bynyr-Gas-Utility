# staff/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from django.contrib.auth.models import User
from requests.models import ServiceRequest
from tracking.services import TrackingService
from tracking.models import RequestStatus

def staff_check(user):
    return user.is_staff

@user_passes_test(staff_check)
def dashboard(request):
    # Get request statistics
    stats = {
        'total_requests': ServiceRequest.objects.count(),
        'pending_requests': ServiceRequest.objects.filter(status='pending').count(),
        'priority_requests': ServiceRequest.objects.filter(status='priority').count(),
        'completed_today': ServiceRequest.objects.filter(
            completed_date__date=timezone.now().date()
        ).count(),
    }
    
    # Get recent requests
    recent_requests = ServiceRequest.objects.select_related(
        'customer', 'request_type'
    ).order_by('-created_at')[:10]
    
    # Get requests assigned to current staff member
    assigned_requests = ServiceRequest.objects.filter(
        assigned_to=request.user
    ).select_related('customer', 'request_type')
    
    context = {
        'stats': stats,
        'recent_requests': recent_requests,
        'assigned_requests': assigned_requests,
    }
    return render(request, 'staff/dashboard.html', context)

@user_passes_test(staff_check)
def request_management(request):
    # Get filters from query parameters
    status = request.GET.get('status')
    priority = request.GET.get('priority')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    search = request.GET.get('search')
    
    # Start with all requests
    requests = ServiceRequest.objects.all()
    
    # Apply filters
    if status:
        requests = requests.filter(status=status)
    if priority:
        requests = requests.filter(status='priority')
    if date_from:
        requests = requests.filter(created_at__gte=date_from)
    if date_to:
        requests = requests.filter(created_at__lte=date_to)
    if search:
        requests = requests.filter(
            Q(customer__username__icontains=search) |
            Q(description__icontains=search) |
            Q(id__icontains=search)
        )
    
    context = {
        'requests': requests,
        'current_filters': request.GET,
    }
    return render(request, 'staff/request_management.html', context)

@user_passes_test(staff_check)
def request_detail(request, pk):
    """
    View for displaying detailed information about a specific service request.
    Includes request details, status history, and customer information.
    """
    service_request = get_object_or_404(ServiceRequest.objects.select_related(
        'customer', 'request_type', 'assigned_to'
    ), pk=pk)
    
    # Get status history
    status_history = RequestStatus.objects.filter(
        service_request=service_request
    ).select_related('created_by').order_by('-created_at')
    
    # Get available staff members for assignment
    available_staff = User.objects.filter(is_staff=True)
    
    context = {
        'service_request': service_request,
        'status_history': status_history,
        'available_staff': available_staff,
        'status_choices': ServiceRequest.STATUS_CHOICES,
    }
    return render(request, 'staff/request_detail.html', context)

@user_passes_test(staff_check)
def update_request(request, pk):
    service_request = get_object_or_404(ServiceRequest, pk=pk)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        notes = request.POST.get('notes')
        assigned_to_id = request.POST.get('assigned_to')
        
        # Update request status
        if new_status:
            service_request.status = new_status
            if new_status == 'completed':
                service_request.completed_date = timezone.now()
        
        # Update assignment
        if assigned_to_id:
            service_request.assigned_to_id = assigned_to_id
        
        service_request.save()
        
        # Create status update and notifications
        TrackingService.create_status_update(
            service_request=service_request,
            new_status=new_status,
            notes=notes,
            user=request.user
        )
        
        messages.success(request, 'Request updated successfully')
        return redirect('staff:request_detail', pk=pk)
    
    context = {
        'service_request': service_request,
    }
    return render(request, 'staff/update_request.html', context)