from rest_framework import serializers
from .models import User, Patient, Therapist, Availability, Appointment, Payment, Notification, SessionRoom

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'role', 'is_verified']

# Patient Serializer
class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Patient
        fields = ['id', 'user', 'date_of_birth', 'gender', 'medical_history', 'preferred_therapist']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)
        patient = Patient.objects.create(user=user, **validated_data)
        return patient
# Therapist Serializer
class TherapistSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Nested user info

    class Meta:
        model = Therapist
        fields = ['id', 'user', 'specialization', 'years_of_experience', 'bio', 'certifications', 'hourly_rate', 'availability_status']

# Availability Serializer
class AvailabilitySerializer(serializers.ModelSerializer):
    therapist = TherapistSerializer()

    class Meta:
        model = Availability
        fields = ['id', 'therapist', 'date', 'start_time', 'end_time', 'is_booked']

# Appointment Serializer
class AppointmentSerializer(serializers.ModelSerializer):
    patient = PatientSerializer()
    therapist = TherapistSerializer()

    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'therapist', 'date', 'start_time', 'end_time', 'status', 'payment_status', 'rescheduled_from']

# Payment Serializer
class PaymentSerializer(serializers.ModelSerializer):
    appointment = AppointmentSerializer()

    class Meta:
        model = Payment
        fields = ['id', 'patient', 'appointment', 'amount', 'payment_method', 'transaction_id', 'payment_status', 'payment_date']

# Notification Serializer
class NotificationSerializer(serializers.ModelSerializer):
    recipient = UserSerializer()

    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'message', 'notification_type', 'is_read', 'created_at']

# Session Room Serializer
class SessionRoomSerializer(serializers.ModelSerializer):
    appointment = AppointmentSerializer()

    class Meta:
        model = SessionRoom
        fields = ['id', 'appointment', 'room_link', 'session_status', 'created_at']
