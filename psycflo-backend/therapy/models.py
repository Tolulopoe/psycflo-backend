from django.db import models
from django.contrib.auth.models import AbstractUser,Group,Permission

class User(AbstractUser):
    ROLE_CHOICES = (
        ('patient', 'Patient'),
        ('therapist', 'Therapist'),
        ('admin', 'Admin'),
    )
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    is_verified = models.BooleanField(default=False)

    username = None  # Remove default username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    groups = models.ManyToManyField(Group, related_name="custom_user_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="custom_user_permissions", blank=True)

# Patient Model
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient')
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    medical_history = models.TextField(blank=True, null=True)
    preferred_therapist = models.ForeignKey('Therapist', on_delete=models.SET_NULL, null=True, blank=True)

# Therapist Model
class Therapist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='therapist')
    specialization = models.CharField(max_length=255)
    years_of_experience = models.IntegerField()
    bio = models.TextField()
    certifications = models.FileField(upload_to='certifications/', blank=True, null=True)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    availability_status = models.BooleanField(default=True)

# Availability Model
class Availability(models.Model):
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_booked = models.BooleanField(default=False)

# Appointment Model
class Appointment(models.Model):
    STATUS_CHOICES = [('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled'), ('completed', 'Completed')]
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('paid', 'Paid'), ('refunded', 'Refunded')])
    rescheduled_from = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

# Payment Model
class Payment(models.Model):
    PAYMENT_METHODS = [('card', 'Card'), ('mobile_money', 'Mobile Money'), ('paypal', 'PayPal')]
    PAYMENT_STATUS = [('success', 'Success'), ('failed', 'Failed'), ('pending', 'Pending')]
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    transaction_id = models.CharField(max_length=100, unique=True)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS, default='pending')
    payment_date = models.DateTimeField(auto_now_add=True)

# Notification Model
class Notification(models.Model):
    NOTIFICATION_TYPES = [('booking', 'Booking'), ('payment', 'Payment'), ('reminder', 'Reminder')]
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

# Session Room Model
class SessionRoom(models.Model):
    SESSION_STATUS = [('not_started', 'Not Started'), ('in_progress', 'In Progress'), ('completed', 'Completed')]
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    room_link = models.URLField()
    session_status = models.CharField(max_length=15, choices=SESSION_STATUS, default='not_started')
    created_at = models.DateTimeField(auto_now_add=True)

