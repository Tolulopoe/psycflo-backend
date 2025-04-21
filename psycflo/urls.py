"""
URL configuration for psycflo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.views.generic.base import RedirectView
from django.http import JsonResponse
from mood_tracker.views import MoodEntryCreateView

def home(request):
    return JsonResponse({"message": "Welcome to PsycFlo API"})



urlpatterns = [
     path('', home),  # Base endpoint
     path('admin/', admin.site.urls),
     path('api/therapy/', include('therapy.urls')),
     path('api/aid/', include('aid.urls')),
     #path('api/', include('users.urls')),
     path('api/community/', include('community.urls')),
     path('api/mood-entry/', MoodEntryCreateView.as_view(), name='mood-entry-create'),  # Mood entry endpoint

     #below is to show a home page view to the api for the community page it can be modified later, redirecting to the posts page.
     # just to avoid Page not found (404) error at /api/community/
     path('', RedirectView.as_view(url='/api/community/posts/', permanent=False), name='home'),

]
