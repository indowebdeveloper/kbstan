from django.urls import path
from .views import CustomerListView, CustomerEditView,\
                    CustomerSignUpView, customerProfile, \
                    customer_create_view, CustomerAddressEditView, CustomerCarEditView, \
                    customer_facing_profile_edit_view, customer_details_view, \
                    CustomerCarDeleteView, CustomerAddressDeleteView, \
                    CustomerAddressCreateView, CustomerCarCreateView, \
                    CustomerFacingAddressCreateView, \
                    CustomerFacingAddressEditView, \
                    CustomerFacingAddressDeleteView, \
                    CustomerFacingCarCreateView, CustomerFacingCarEditView, CustomerFacingCarDeleteView

urlpatterns = [
    ## customer facing urls
    # path('signup/', CustomerSignUpView.as_view(), name='customer-signup'),  #? depricated and replaced by accounts/signup from allauth 
    path('profile/', customerProfile, name='customer-profile'),
    path('profile/edit/', customer_facing_profile_edit_view, name='customer-profile-edit'),
    path('profile/<int:customer_pk>/address/create/', CustomerFacingAddressCreateView.as_view(), name='customer-facing-address-create'),
    path('profile/<int:pk>/address/edit/', CustomerFacingAddressEditView.as_view(), name='customer-facing-address-edit'),
    path('profile/<int:pk>/address/delete/', CustomerFacingAddressDeleteView.as_view(), name='customer-facing-address-delete'),
  
    path('profile/<int:customer_pk>/car/create/', CustomerFacingCarCreateView.as_view(), name='customer-facing-car-create'),
    path('profile/<int:pk>/car/edit/', CustomerFacingCarEditView.as_view(), name='customer-facing-car-edit'),
    path('profile/<int:pk>/car/delete/', CustomerFacingCarDeleteView.as_view(), name='customer-facing-car-delete'),  

    ## backoffice urls
    path('', CustomerListView.as_view(), name='customer-list'),
    path('create/', customer_create_view, name='customer-create'),
    path('<int:pk>/', customer_details_view, name='customer-details'),
    path('<int:pk>/edit/', CustomerEditView.as_view(), name='customer-edit'),

    path('<int:customer_pk>/address/create/', CustomerAddressCreateView.as_view(), name='customer-address-create'),
    path('<int:pk>/address/edit/', CustomerAddressEditView.as_view(), name='customer-address-edit'),
    path('<int:pk>/address/delete/', CustomerAddressDeleteView.as_view(), name='customer-address-delete'),

    path('<int:customer_pk>/car/create/', CustomerCarCreateView.as_view(), name='customer-car-create'),
    path('<int:pk>/car/edit/', CustomerCarEditView.as_view(), name='customer-car-edit'),
    path('<int:pk>/car/delete/', CustomerCarDeleteView.as_view(), name='customer-car-delete'),
]