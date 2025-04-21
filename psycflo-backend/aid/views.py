from django.http import HttpResponse
from django.template import loader
from .models import AidRequest ,donors

def aid_objects(request):
    aids = AidRequest.objects.all()
    template = loader.get_template('Aidobjects.html')
    context = {
        'aids': aids,  
    }
    return HttpResponse(template.render(context, request))



def donating(request):
    donors = donors.objects.all()
    template = loader.get_template('Aidobjects.html')
    context = {
        'donors': donors,  
    }
    return HttpResponse(template.render(context, request))



from rest_framework import generics
from .serializers import AidRequestSerializer,donorsSerializer

class AidRequestCreateView(generics.CreateAPIView):
    queryset = AidRequest.objects.all()
    serializer_class = AidRequestSerializer

class donorsCreateView(generics.CreateAPIView):
    queryset = donors.objects.all()
    serializer_class = donorsSerializer

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class AidRequestListView(generics.ListAPIView):
    queryset = AidRequest.objects.all()
    serializer_class = AidRequestSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['fullname']  
    search_fields = ['fullname', 'email', 'country']

class donorsListView(generics.ListAPIView):
    queryset = donors.objects.all()
    serializer_class = donorsSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['brandname']  
    search_fields = ['brandname', 'donated_at', 'distributed']
