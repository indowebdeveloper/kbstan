from django.urls import path
from . import views

urlpatterns = [
    ## CF Views
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('terms-of-use/', views.terms_of_use, name='terms-of-use'),
    path('privacy-policy/', views.privacy_policy, name='privacy-policy'),

    ## BO Views
    # path('pages-content/list/', views.pages_content_list, name='page-content-list'),
    path('pagecontent/edit/<int:pk>/', views.PageContentEditView.as_view(), name='pagecontent-edit'),

    # Product Sections
    path('productsection/list/', views.product_section_list_view, name='productsection-list'),
    path('productsection/create/', views.ProductSectionCreateView.as_view(), name='productsection-create'),
    path('productsection/edit/<int:pk>/', views.ProductSectionEditView.as_view(), name='productsection-edit'),
    path('productsection/delete/<int:pk>/', views.ProductSectionDeleteView.as_view(), name='productsection-delete'),

    # Product Brands
    path('productbrand/list/', views.product_brands_list_view, name='productbrand-list'),
    path('productbrand/create/', views.ProductBrandCreateView.as_view(), name='productbrand-create'),
    path('productbrand/edit/<int:pk>/', views.ProductBrandEditView.as_view(), name='productbrand-edit'),
    path('productbrand/delete/<int:pk>/', views.ProductBrandDeleteView.as_view(), name='productbrand-delete'),
    
    # Email Contents
    path('emailcontent/list/', views.email_content_list_view, name='emailcontent-list'),
    path('emailcontent/create/', views.EmailContentCreateView.as_view(), name='emailcontent-create'),
    path('emailcontent/edit/<int:pk>/', views.EmailContentEditView.as_view(), name='emailcontent-edit'),
    path('emailcontent/delete/<int:pk>/', views.EmailContentDeleteView.as_view(), name='emailcontent-delete'),
]