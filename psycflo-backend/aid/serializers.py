from rest_framework import serializers
from .models import AidRequest,donors

class AidRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = AidRequest
        fields = '__all__'

class donorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = donors
        fields = '__all__'
