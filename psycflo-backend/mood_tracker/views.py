from django.shortcuts import render

from rest_framework import viewsets, permissions
from rest_framework.exceptions import ValidationError
from rest_framework import generics
from .models import MoodEntry
from .serializers import MoodEntrySerializer

class MoodEntryCreateView(generics.CreateAPIView):
    queryset = MoodEntry.objects.all()
    serializer_class = MoodEntrySerializer
from datetime import date

class MoodTrackerViewSet(viewsets.ModelViewSet):
    serializer_class = MoodEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # return MoodTracker.objects.filter(patient__user=self.request.user)
        # patient = self.request.user.patient
        # today = serializers.validated_data.get('date', None)
        return MoodEntry.objects.filter(patient__user=self.request.user)
    
        if MoodEntry.objects.filter(patient=patient, date__exact=today).exists():
            raise ValidationError("You have already submitted a mood entry today.")

    def perform_create(self, serializer):
        patient = self.request.user.patient
        today = date.today()

        if MoodEntry.objects.filter(patient=patient, date=today).exists():
            raise ValidationError("You have already submitted a mood entry today.")

        serializer.save(patient=patient)

# class MoodEntryCreateView(generics.CreateAPIView):
#     queryset = MoodEntry.objects.all()
#     serializer_class = MoodEntrySerializer
#     permission_classes = [IsAuthenticated]
    
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

# Create your views here.
