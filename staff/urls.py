# staff/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'staff'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/staff_login.html'), name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('requests/', views.request_management, name='request_management'),
    path('request/<int:pk>/', views.request_detail, name='request_detail'),
    path('request/<int:pk>/update/', views.update_request, name='update_request'),
]