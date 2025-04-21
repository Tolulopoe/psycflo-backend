from django.urls import path
from .views import MoodEntryCreateView

urlpatterns = [
    path('api/mood-entry/', MoodEntryCreateView.as_view(), name='mood-entry-create'),
]


# from rest_framework.routers import DefaultRouter
# from .views import MoodTrackerViewSet

# router = DefaultRouter()
# router.register(r'mood-tracker', MoodTrackerViewSet, basename='mood-tracker')

# urlpatterns += router.urls

# class MoodTrackerViewSet(viewsets.ModelViewSet):
#     serializer_class = MoodTrackerSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return MoodTracker.objects.filter(patient__user=self.request.user)

#     def perform_create(self, serializer):
#         serializer.save(patient=self.request.user.patient)