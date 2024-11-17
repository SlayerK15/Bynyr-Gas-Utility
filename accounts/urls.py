# accounts/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import CustomLogoutView

app_name = 'accounts'

urlpatterns = [
    path('register/', views.customer_register, name='register'),
    path('staff/register/', views.staff_register, name='staff_register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('dashboard/', views.customer_dashboard, name='customer_dashboard'),
]