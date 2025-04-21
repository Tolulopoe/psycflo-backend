from django.urls import path

from .views import AidRequestCreateView, AidRequestListView, donorsCreateView, donorsListView

from .views import AidRequestCreateView, AidRequestListView


urlpatterns = [
    path('', AidRequestListView.as_view(), name='aid-list'),
    path('create/', AidRequestCreateView.as_view(), name='aid-create'),
    path('list/', AidRequestListView.as_view(), name='aid-list'),


    path('', donorsListView.as_view(), name='donors-list'),
    path('create/',donorsCreateView.as_view(), name='donors-create'),
    path('list/', donorsListView.as_view(), name='donors-list'),
]

]

