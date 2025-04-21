from django.urls import path
from .views import chatbot_real


urlpatterns = [
    path('talk/', chatbot_real, name='chatbot'),
]
