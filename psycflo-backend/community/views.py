from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from django.utils import timezone
from .models import *
from .serializers import *

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Post.objects.all()  # Added this line

    def get_queryset(self):
        queryset = Post.objects.published().select_related('author', 'category')

        if self.request.query_params.get('category'):
            queryset = queryset.filter(category__slug=self.request.query_params.get('category'))

        if self.request.query_params.get('trending'):
            queryset = queryset.order_by('-engagement_score')[:20]

        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        """Increment views count when a post is retrieved."""
        instance = self.get_object()
        instance.views += 1
        instance.engagement_score = instance.calculate_engagement_score()
        instance.save(update_fields=['views', 'engagement_score'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def share(self, request, pk=None):
        """Increment shares count for a post."""
        try:
            post = self.get_object()
            post.shares += 1
            post.engagement_score = post.calculate_engagement_score()
            post.save(update_fields=['shares', 'engagement_score'])
            return Response({'message': 'Post shared successfully.'}, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def register(self, request, pk=None):
        with transaction.atomic():
            event = Event.objects.select_for_update().get(pk=pk)

            if event.registration_deadline and event.registration_deadline < timezone.now():
                return Response({'error': 'Registration closed'}, status=status.HTTP_400_BAD_REQUEST)

            if event.available_seats <= 0:
                return Response({'error': 'Event is full'}, status=status.HTTP_400_BAD_REQUEST)

            if EventRegistration.objects.filter(event=event, user=request.user).exists():
                return Response({'error': 'Already registered'}, status=status.HTTP_400_BAD_REQUEST)

            registration = EventRegistration.objects.create(event=event, user=request.user)
            return Response(
                EventRegistrationSerializer(registration).data,
                status=status.HTTP_201_CREATED
            )

class UserProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)