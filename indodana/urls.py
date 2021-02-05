from django.urls import path
from . import views


urlpatterns = [
    path('', views.debug, name='indodana-debug'),
]
