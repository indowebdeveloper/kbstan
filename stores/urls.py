from django.urls import path
from . import views

urlpatterns = [
    path('', views.stores, name='stores'),
    path('list/', views.stores_list, name='stores-list'),
    path('create/', views.StoreCreateView.as_view(), name='stores-create'),
    path('update/<int:pk>/', views.StoreUpdateView.as_view(), name='stores-update'),
    path('delete/<int:pk>/', views.StoreDeleteView.as_view(), name='stores-delete'),
]