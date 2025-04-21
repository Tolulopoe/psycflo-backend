from django.db import models

def __str__(self):
        return f"User: {self.user_input[:30]}..."

class ChatbotMessage(models.Model):
  

    def __str__(self):
        return f"{self.user} at {self.timestamp}"

class ChatSession(models.Model):

    session_id = models.CharField(max_length=100, unique=True)
    user_id = models.IntegerField(blank=True, null=True)  # Optional: link to user
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    def __str__(self):
        return f"Session {self.session_id} | Started at {self.started_at}"


class ChatMessage(models.Model):
    user = models.CharField(max_length=100)
    user_input = models.TextField()
    bot_response = models.TextField()
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=10, choices=(('user', 'User'), ('bot', 'Bot')))
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    intent_detected = models.CharField(max_length=100, blank=True)
    is_follow_up = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender} at {self.timestamp}: {self.message[:30]}"
