from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.service_list_view, name='service-list'),

    path('create/', views.ServiceCreateView.as_view(), name='service-create'),
    path('<slug:slug>/view', views.ServiceDetailsView.as_view(), name='service-details'),
    path('<slug:slug>/edit/', views.ServiceEditView.as_view(), name='service-edit'),
    path('<slug:slug>/delete/', views.ServiceDeleteView.as_view(), name='service-delete'),

    # Customer view urls
    # path('', views.customer_services_list_view, name='services'),
    # path('<slug:slug>/', views.CustomerServiceDetailsView.as_view(), name='service'),
]
