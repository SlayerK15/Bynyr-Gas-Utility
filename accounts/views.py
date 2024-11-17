# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db import transaction

from accounts.forms import CustomerRegistrationForm, StaffRegistrationForm
from accounts.models import CustomerProfile, StaffProfile

def home(request):
    return render(request, 'home.html')

@transaction.atomic
def customer_register(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            try:
                # Check if email already exists
                email = form.cleaned_data.get('email')
                if form.cleaned_data.get('email'):
                    if request.user.is_authenticated:
                        messages.error(request, 'You are already logged in.')
                        return redirect('accounts:customer_dashboard')
                
                # Create user and profile in a transaction
                user = form.save(commit=False)
                user.is_staff = False
                user.save()
                
                # Delete any existing profile (shouldn't exist, but just in case)
                CustomerProfile.objects.filter(user=user).delete()
                
                # Create new profile
                CustomerProfile.objects.create(
                    user=user,
                    phone_number=form.cleaned_data['phone_number'],
                    address=form.cleaned_data['address'],
                    customer_id=f"CUST{user.id:06d}"
                )
                
                login(request, user)
                messages.success(request, 'Account created successfully!')
                return redirect('accounts:customer_dashboard')
            
            except Exception as e:
                messages.error(request, f'Registration failed: {str(e)}')
                return render(request, 'accounts/register.html', {'form': form})
    else:
        form = CustomerRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
@transaction.atomic
def staff_register(request):
    if request.method == 'POST':
        form = StaffRegistrationForm(request.POST)
        if form.is_valid():
            try:
                # Create user and profile in a transaction
                user = form.save(commit=False)
                user.is_staff = True
                user.save()
                
                # Delete any existing profile
                StaffProfile.objects.filter(user=user).delete()
                
                # Create new profile
                StaffProfile.objects.create(
                    user=user,
                    department=form.cleaned_data['department'],
                    designation=form.cleaned_data['designation'],
                    is_supervisor=form.cleaned_data.get('is_supervisor', False),
                    employee_id=f"EMP{user.id:06d}"
                )
                
                messages.success(request, 'Staff account created successfully!')
                return redirect('staff:dashboard')
                
            except Exception as e:
                messages.error(request, f'Staff registration failed: {str(e)}')
                return render(request, 'accounts/staff_register.html', {'form': form})
    else:
        form = StaffRegistrationForm()
    return render(request, 'accounts/staff_register.html', {'form': form})


from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db import transaction
from django.db.models import Q, Count
from django.utils import timezone

from accounts.forms import CustomerRegistrationForm, StaffRegistrationForm
from accounts.models import CustomerProfile, StaffProfile
from requests.models import ServiceRequest

# Keep your existing customer_register and staff_register views...

@login_required(login_url='home')
def customer_dashboard(request):
    # Check if user is staff and redirect if necessary
    if request.user.is_staff:
        messages.warning(request, 'Staff members should use the staff dashboard.')
        return redirect('staff:dashboard')
    
    try:
        # Get customer profile and related data
        profile = request.user.customerprofile
        
        # Get service request statistics
        stats = {
            'total_requests': ServiceRequest.objects.filter(
                customer=request.user
            ).count(),
            'pending_requests': ServiceRequest.objects.filter(
                customer=request.user,
                status='pending'
            ).count(),
            'in_progress_requests': ServiceRequest.objects.filter(
                customer=request.user,
                status__in=['assigned', 'in_progress']
            ).count(),
            'completed_requests': ServiceRequest.objects.filter(
                customer=request.user,
                status='completed'
            ).count()
        }
        
        # Get recent requests with all related data
        recent_requests = ServiceRequest.objects.filter(
            customer=request.user
        ).select_related(
            'request_type'
        ).order_by(
            '-created_at'
        )[:5]
        
        # Check for priority requests
        priority_requests = ServiceRequest.objects.filter(
            customer=request.user,
            status='priority',
            created_at__gte=timezone.now() - timezone.timedelta(days=7)
        ).exists()
        
        if priority_requests:
            messages.warning(
                request,
                'You have priority service requests that require attention.'
            )
        
        context = {
            'profile': profile,
            'stats': stats,
            'recent_requests': recent_requests,
            'last_login': request.user.last_login,
        }
        
        return render(request, 'accounts/customer_dashboard.html', context)
        
    except CustomerProfile.DoesNotExist:
        messages.error(request, 'Customer profile not found. Please contact support.')
        logout(request)
        return redirect('accounts:login')
    except Exception as e:
        messages.error(request, f'An error occurred loading your dashboard: {str(e)}')
        return redirect('accounts:login')

@user_passes_test(lambda u: u.is_staff, login_url='home')
@login_required(login_url='home')
def staff_dashboard(request):
    ...

# Keep your existing custom_login_required decorator but add staff check
def custom_login_required(view_func):
    """Custom decorator to handle login and profile checks"""
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        # Check if user is staff
        if request.user.is_staff:
            messages.warning(request, 'Staff members should use the staff dashboard.')
            return redirect('staff:dashboard')
        
        # Check for customer profile
        if not hasattr(request.user, 'customerprofile'):
            messages.error(request, 'Invalid account type or profile not found.')
            logout(request)
            return redirect('accounts:login')
            
        return view_func(request, *args, **kwargs)
    return _wrapped_view

from django.views import View

class CustomLogoutView(View):
    def post(self, request):
        logout(request)
        return redirect('home')