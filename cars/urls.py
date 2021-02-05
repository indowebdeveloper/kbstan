from django.urls import path
from .views import cars, carBrandCreate, carModelCreate, carBrandUpdate, carModelUpdate, carBrandDelete, carModelDelete

urlpatterns = [
    path('', cars, name='cars'),

    # API endpoints
    path('carbrand/create/', carBrandCreate),
    path('carmodel/create/', carModelCreate),
    path('carbrand/update/', carBrandUpdate),
    path('carmodel/update/', carModelUpdate),
    path('carbrand/delete/', carBrandDelete),
    path('carmodel/delete/', carModelDelete),
]