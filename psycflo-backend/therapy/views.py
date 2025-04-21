from django.shortcuts import render
from rest_framework import generics
from .models import User, Patient, Therapist, Availability, Appointment, Payment, Notification, SessionRoom
from .serializers import (
    UserSerializer, PatientSerializer, TherapistSerializer, AvailabilitySerializer, 
    AppointmentSerializer, PaymentSerializer, NotificationSerializer, SessionRoomSerializer
)

# User Views
class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Patient Views
class PatientListCreateView(generics.ListCreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class PatientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

# Therapist Views
class TherapistListCreateView(generics.ListCreateAPIView):
    queryset = Therapist.objects.all()
    serializer_class = TherapistSerializer

class TherapistDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Therapist.objects.all()
    serializer_class = TherapistSerializer

# Availability Views
class AvailabilityListCreateView(generics.ListCreateAPIView):
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer

class AvailabilityDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer

# Appointment Views
class AppointmentListCreateView(generics.ListCreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

class AppointmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

# Payment Views
class PaymentListCreateView(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class PaymentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

# Notification Views
class NotificationListCreateView(generics.ListCreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

class NotificationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

# Session Room Views
class SessionRoomListCreateView(generics.ListCreateAPIView):
    queryset = SessionRoom.objects.all()
    serializer_class = SessionRoomSerializer

class SessionRoomDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SessionRoom.objects.all()
    serializer_class = SessionRoomSerializer
