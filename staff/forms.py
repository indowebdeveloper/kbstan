from django import forms
from customers.models import User
from .models import Staff
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from allauth.account.forms import SignupForm 


class StaffPermissionsForm(forms.Form):
    dashboard = forms.BooleanField(required=False)
    pagecontent = forms.BooleanField(required=False, label='Website Content')
    product = forms.BooleanField(required=False, label='Products')
    order = forms.BooleanField(required=False, label='Orders')
    customer = forms.BooleanField(required=False, label='Customers')
    carbrand = forms.BooleanField(required=False, label='Cars')
    staff = forms.BooleanField(required=False, label='Staff')
    store = forms.BooleanField(required=False, label='Stores')
    coupon = forms.BooleanField(required=False, label='Coupons')
    promotion = forms.BooleanField(required=False, label='Promotions')


class StaffSignUpForm(SignupForm): 
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
        user = super(StaffSignUpForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.mobileNumber = self.cleaned_data['mobileNumber']

        user.isStaff = True
        user.save()
        # staff = Staff.objects.create(user=user)
        return user


class StaffFaceEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'mobileNumber',
        ]


#? delete this form in not used in production???
class UserCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'password',
            # 'password1',
            # 'password2',
            # 'phoneNumber',
            'mobileNumber',
        ]

#? delete this form in not used in production???
class StaffCreateForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = [
            'sectionsAccess',
        ]


#? delete this form in not used in production???
class StaffCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'email', 
                    # 'phoneNumber',
                    'mobileNumber')

    #* earlier function for save
    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     user.isStaff = True
    #     if commit:
    #         user.save()
    #     return user

    #* same function as for customer
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.isStaff = True
        user.save()
        customer = Staff.objects.create(user=user)
        return user
