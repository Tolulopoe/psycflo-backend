from django.urls import path
from .views import (
    UserListCreateView, UserDetailView,
    PatientListCreateView, PatientDetailView,
    TherapistListCreateView, TherapistDetailView,
    AvailabilityListCreateView, AvailabilityDetailView,
    AppointmentListCreateView, AppointmentDetailView,
    PaymentListCreateView, PaymentDetailView,
    NotificationListCreateView, NotificationDetailView,
    SessionRoomListCreateView, SessionRoomDetailView
)

urlpatterns = [
    # User URLs
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),

    # Patient URLs
    path('patients/', PatientListCreateView.as_view(), name='patient-list-create'),
    path('patients/<int:pk>/', PatientDetailView.as_view(), name='patient-detail'),

    # Therapist URLs
    path('therapists/', TherapistListCreateView.as_view(), name='therapist-list-create'),
    path('therapists/<int:pk>/', TherapistDetailView.as_view(), name='therapist-detail'),

    # Availability URLs
    path('availability/', AvailabilityListCreateView.as_view(), name='availability-list-create'),
    path('availability/<int:pk>/', AvailabilityDetailView.as_view(), name='availability-detail'),

    # Appointment URLs
    path('appointments/', AppointmentListCreateView.as_view(), name='appointment-list-create'),
    path('appointments/<int:pk>/', AppointmentDetailView.as_view(), name='appointment-detail'),

    # Payment URLs
    path('payments/', PaymentListCreateView.as_view(), name='payment-list-create'),
    path('payments/<int:pk>/', PaymentDetailView.as_view(), name='payment-detail'),

    # Notification URLs
    path('notifications/', NotificationListCreateView.as_view(), name='notification-list-create'),
    path('notifications/<int:pk>/', NotificationDetailView.as_view(), name='notification-detail'),

    # Session Room URLs
    path('session-rooms/', SessionRoomListCreateView.as_view(), name='sessionroom-list-create'),
    path('session-rooms/<int:pk>/', SessionRoomDetailView.as_view(), name='sessionroom-detail'),
]