from django.urls import path
from . import views

urlpatterns = [
    path('', views.coupon_list_view, name='coupon-list'),
    path('create/', views.coupon_create_view, name='coupon-create'),
    path('<int:pk>/edit/', views.coupon_edit_view, name='coupon-edit'),
    path('<int:pk>/delete/', views.CouponDeleteView.as_view(), name='coupon-delete'),
]
