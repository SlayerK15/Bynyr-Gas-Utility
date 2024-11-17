# requests/urls.py
from django.urls import path
from . import views

app_name = 'requests'

urlpatterns = [
    path('create/', views.create_request, name='create_request'),
    path('<int:pk>/', views.request_detail, name='request_detail'),
    path('list/', views.request_list, name='request_list'),
    path('<int:pk>/update/', views.update_request, name='update_request'),
    path('<int:pk>/cancel/', views.cancel_request, name='cancel_request'),
]
