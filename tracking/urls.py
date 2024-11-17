# tracking/urls.py
from django.urls import path
from . import views

app_name = 'tracking'

urlpatterns = [
    path('request/<int:request_id>/', views.track_request, name='track_request'),
    path('request/<int:request_id>/timeline/', views.request_timeline, name='timeline'),
    path('notifications/', views.notifications_list, name='notifications'),
    path('notifications/<int:notification_id>/mark-read/', 
         views.mark_notification_read, name='mark_notification_read'),
]