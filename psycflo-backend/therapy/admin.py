from django.contrib import admin
from .models import User, Patient, SessionRoom,Notification,Payment,Appointment,Therapist,Availability

# Register your models here.
admin.site.register(User)
admin.site.register(Patient)
admin.site.register(SessionRoom)
admin.site.register(Notification)
admin.site.register(Payment)
admin.site.register(Appointment)
admin.site.register(Therapist)
