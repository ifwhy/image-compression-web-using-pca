from django.urls import path

from .views import index, download 

urlpatterns = [
    path('', index, name='index'),
    path('download/', download, name='download'),
]
