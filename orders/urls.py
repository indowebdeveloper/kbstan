from django.urls import path
from . import views

urlpatterns = [
    ## BACKOFFICE FACING VIEWS
    path('', views.OrderListView.as_view(), name='order-list'),
    path('create/', views.order_create_view, name='order-create'),
    path('create/<int:pk>/', views.order_create_cart_view, name='order-create-cart'),
    path('<int:pk>/', views.OrderDetailsView.as_view(), name='order-details'),
    path('<int:pk>/edit/', views.OrderEditView.as_view(), name='order-edit'),

    # order iteams 
    path('orderitem/<int:pk>/edit/', views.OrderItemEditView.as_view(), name='orderitem-edit'),


    ## CUSTOMER facing views
    path('list/', views.customer_orders, name='customer-orders'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('customer-enquiry/<slug:slug>/', views.customer_enquiry, name='customer-enquiry'),


    ## API endpoints
    path('create/select_products/', views.select_products, name='order-create-select-products'),
    path('update_cart/', views.update_cart, name='update-cart'),
    path('select_customer/', views.select_customer, name='select-customer'),

    ## INDODANA endpoints
    path('transaction-approval/', views.transaction_approval_view),
]
