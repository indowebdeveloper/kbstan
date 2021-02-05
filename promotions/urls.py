from django.urls import path
from . import views

urlpatterns = [
    path('', views.promotion_list_view, name='promotion-list'),
    path('create/', views.promotion_create_view, name='promotion-create'),
    path('<int:pk>/edit/', views.promotion_edit_view, name='promotion-edit'),
    path('<int:pk>/delete/', views.PromotionDeleteView.as_view(), name='promotion-delete'),
]
