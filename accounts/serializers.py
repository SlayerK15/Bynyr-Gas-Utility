# accounts/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import CustomerProfile, StaffProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_staff')

class CustomerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = CustomerProfile
        fields = ('id', 'user', 'customer_id', 'phone_number', 'address')

class StaffProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = StaffProfile
        fields = ('id', 'user', 'employee_id', 'department', 'designation')