from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from requests.models import ServiceRequest

class StaffShift(models.Model):
    """Staff work shift schedules"""
    SHIFT_TYPES = [
        ('morning', 'Morning (6AM-2PM)'),
        ('afternoon', 'Afternoon (2PM-10PM)'),
        ('night', 'Night (10PM-6AM)'),
        ('custom', 'Custom Hours')
    ]

    staff = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shifts')
    shift_type = models.CharField(max_length=20, choices=SHIFT_TYPES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    days_of_week = models.CharField(max_length=50)  # Stored as comma-separated numbers (0-6)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['start_time']

    def __str__(self):
        return f"{self.staff.username} - {self.get_shift_type_display()}"

class StaffSpecialization(models.Model):
    """Staff specializations and skills"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    required_certification = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class StaffProfile(models.Model):
    """Extended staff profile information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff_profile')
    employee_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    specializations = models.ManyToManyField(StaffSpecialization)
    supervisor = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='supervised_staff'
    )
    max_active_requests = models.IntegerField(default=10)
    can_escalate = models.BooleanField(default=False)
    is_supervisor = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.employee_id})"

class WorkloadMetrics(models.Model):
    """Track staff workload metrics"""
    staff = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workload_metrics')
    date = models.DateField()
    active_requests = models.IntegerField(default=0)
    completed_requests = models.IntegerField(default=0)
    average_resolution_time = models.DurationField(null=True)
    customer_satisfaction_score = models.FloatField(null=True)
    sla_compliance_rate = models.FloatField(default=0.0)

    class Meta:
        unique_together = ['staff', 'date']
        ordering = ['-date']

    def __str__(self):
        return f"{self.staff.username} metrics for {self.date}"

class StaffNote(models.Model):
    """Internal notes about staff members"""
    staff = models.ForeignKey(User, on_delete=models.CASCADE, related_name='staff_notes')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='authored_notes')
    note_type = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_private = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Note about {self.staff.username} by {self.author.username}"

class PerformanceReview(models.Model):
    """Staff performance reviews"""
    RATING_CHOICES = [
        (1, 'Needs Improvement'),
        (2, 'Meets Some Expectations'),
        (3, 'Meets Expectations'),
        (4, 'Exceeds Expectations'),
        (5, 'Outstanding')
    ]

    staff = models.ForeignKey(User, on_delete=models.CASCADE, related_name='performance_reviews')
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='reviewed_staff')
    review_date = models.DateField()
    period_start = models.DateField()
    period_end = models.DateField()
    rating = models.IntegerField(choices=RATING_CHOICES)
    feedback = models.TextField()
    goals = models.TextField()
    acknowledgement_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-review_date']

    def __str__(self):
        return f"Review for {self.staff.username} on {self.review_date}"