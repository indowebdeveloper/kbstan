from django import forms
# from django.contrib.auth.forms import UserCreationForm
from allauth.account.forms import SignupForm 
from django.db import transaction
from cars.models import CustomerCar

from .models import Customer, User, Address
from staff.models import Staff

# class CustomerSignUpForm(UserCreationForm):

#     class Meta(UserCreationForm.Meta):
#         model = User

#     @transaction.atomic
#     def save(self):
#         user = super().save(commit=False)
#         user.isCustomer = True
#         user.save()
#         customer = Customer.objects.create(user=user)
#         return user


class CustomerSignUpForm(SignupForm): 
    first_name = forms.CharField(max_length=30, label='First Name') 
    last_name = forms.CharField(max_length=30, label='Last Name') 

    mobileNumber = forms.CharField(max_length=15, label='Mobile number')

    field_order = [
    'first_name', 
    'last_name',
    'mobileNumber',
    'email', 
    'password'
    ]
    
    def save(self, request):
        user = super(CustomerSignUpForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.mobileNumber = self.cleaned_data['mobileNumber']
        
        user.isCustomer = True
        user.save()
        customer = Customer.objects.create(user=user)
        
        return user


## Staff creating customer in backoffice form 
class CustomerCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            # 'phoneNumber',
            'mobileNumber',
            # 'is_active'
        ]

class CustomerAddressCreateForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            'type',
            'state',
            'zipCode',
            'city',
            'street',
            'houseNumber',
            'shippingCost',
        ]

class CustomerCarCreateForm(forms.ModelForm):
    class Meta:
        model = CustomerCar
        fields = [
            'carBrand',
            'carModel',
            'licensePlate'
        ]


###  CUSTOMER FACING PROFILE EDIT FORMS  ###

class CustomerFaceContactEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'mobileNumber',
        ]

class CustomerFaceAddressCreateForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            'type',
            'state',
            'zipCode',
            'city',
            'street',
            'houseNumber',
            # 'shippingCost',
        ]
