from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.product_list_view, name='product-list'),
    path('attributes/', views.attributes, name='attributes'),
    path('categories/', views.categories, name='categories'),

    path('create/', views.product_create_view, name='product-create'),
    path('<slug:slug>/view', views.ProductDetailsView.as_view(), name='product-details'),
    path('<slug:slug>/edit/', views.ProductEditView.as_view(), name='product-edit'),
    path('<slug:slug>/delete/', views.ProductDeleteView.as_view(), name='product-delete'),
    path('<slug:slug>/adjust-stock/', views.adjust_stock, name='product-adjust-stock'),

    path('product-attribute/<int:product_pk>/create/', views.ProductAttributeCreateView.as_view(), name='product-attribute-create'),
    path('product-attribute/<int:pk>/edit/', views.ProductAttributeEditView.as_view(), name='product-attribute-edit'),
    path('product-attribute/<int:pk>/delete/', views.ProductAttributeDeleteView.as_view(), name='product-attribute-delete'),
    
    # Customer view urls
    path('', views.customer_products_list_view, name='products'),
    path('<slug:slug>/', views.CustomerProductDetailsView.as_view(), name='product'),

    # API endpoints
    path('attributes/create', views.attributesCreate, name='products-attributes-create'),
    path('attributes/edit', views.attributesUpdate, name='products-attributes-edit'),
    path('attributes/delete', views.attributesDelete, name='products-attributes-delete'),
    path('categories/create', views.categoriesCreate, name='products-categories-create'),
    path('categories/edit', views.categoriesUpdate, name='products-categories-edit'),
    path('categories/delete', views.categoriesDelete, name='products-categories-delete'),
]
