from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.
class MoodEntry(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feeling = models.CharField(max_length=255, help_text="How are you feeling today?")
    improvement_since_last_session = models.BooleanField()
    daily_routine = models.CharField(max_length=255)
    notes = models.TextField(blank=True, null=True)
    date = models.DateField(default=timezone.now)
    # created_at = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now_add=True)

   


    class Meta:
        unique_together = ('user', 'date')  # One mood entry per patient per day

    def __str__(self):
        return f"MoodEntry by {self.user} on {self.timestamp.strftime('%Y-%m-%d')}"