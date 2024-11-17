# tracking/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from requests.models import ServiceRequest
from .models import RequestStatus, Notification

@login_required
def track_request(request, request_id):
    service_request = get_object_or_404(ServiceRequest, id=request_id)
    
    # Ensure user has permission to view this request
    if not request.user.is_staff and request.user != service_request.customer:
        return redirect('accounts:dashboard')
    
    status_updates = RequestStatus.objects.filter(service_request=service_request)
    
    context = {
        'service_request': service_request,
        'status_updates': status_updates,
    }
    return render(request, 'tracking/track_request.html', context)

@login_required
def request_timeline(request, request_id):
    service_request = get_object_or_404(ServiceRequest, id=request_id)
    status_updates = RequestStatus.objects.filter(
        service_request=service_request
    ).select_related('created_by')
    
    context = {
        'service_request': service_request,
        'status_updates': status_updates,
    }
    return render(request, 'tracking/timeline.html', context)

@login_required
def notifications_list(request):
    notifications = Notification.objects.filter(user=request.user)
    unread_count = notifications.filter(read=False).count()
    
    if request.GET.get('mark_all_read'):
        notifications.filter(read=False).update(read=True)
    
    context = {
        'notifications': notifications,
        'unread_count': unread_count,
    }
    return render(request, 'tracking/notifications.html', context)

@login_required
def mark_notification_read(request, notification_id):
    notification = get_object_or_404(
        Notification, 
        id=notification_id, 
        user=request.user
    )
    notification.read = True
    notification.save()
    return JsonResponse({'status': 'success'})
