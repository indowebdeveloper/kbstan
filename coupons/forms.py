from django import forms
from .models import Coupon

class CouponCreateForm(forms.ModelForm):
    class Meta:
        model = Coupon
        # fields = "__all__"
        exclude = ['customersUsedCoupons']
        widgets = {
            'dateStart': forms.DateInput(
                # format=('%d-%m-%Y'), 
                attrs={
                    'type': 'date',
                    # 'format': 'dd-mm-yyyy'
                }
            ),
            'dateEnd': forms.DateInput(
                # format=('%d-%m-%Y'), 
                attrs={
                    'type': 'date',
                    # 'format': 'dd-mm-yyyy'
                }
            ),
        }

class CouponEditForm(forms.ModelForm):
    class Meta:
        model = Coupon
        # fields = "__all__"
        exclude = ['customersUsedCoupons']
        widgets = {
            'dateStart': forms.widgets.DateInput(attrs={'type': 'date'}),
            'dateEnd': forms.widgets.DateInput(attrs={'type': 'date'}),
        }

