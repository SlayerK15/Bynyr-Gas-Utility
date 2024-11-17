# accounts/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    customer_id = models.CharField(max_length=20, unique=True)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile (ID: {self.customer_id})"

class StaffProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=50)
    designation = models.CharField(max_length=50)
    is_supervisor = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Staff Profile (ID: {self.employee_id})"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_staff:
            StaffProfile.objects.create(
                user=instance,
                employee_id=f"EMP{instance.id:06d}"
            )
        else:
            CustomerProfile.objects.create(
                user=instance,
                customer_id=f"CUST{instance.id:06d}"
            )