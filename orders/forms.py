from django import forms
from .models import (
    Order,
    ORDER_CHANNEL_CHOICES,
    PAYMENT_CHOICES,
    INSTALLMENT_CHOICES
)
from .utils import (
    get_stores_choices,
    BANK_CHOICES
)

class OrderEditForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'status',
            # 'orderChannel',
            'store',
            # 'paymentOption',
            # 'product',
            # 'quantity',
            'shippingCost',
            # 'customer',
            # 'staff',
            # 'coupon',
            'notes',
        ]


class QuantityForm(forms.Form):
    quantity = forms.IntegerField(label='Quantity', min_value=1)


# class ProductCollectionForm(forms.Form):
#     product_collection_choices = [
#         ('shipping', 'Shipping delivery'),
#         ('store-pickup', 'Pickup in store'),
#     ]

#     product_collection_method = forms.ChoiceField(choices=product_collection_choices)


class CheckoutPaymentMethodsForm(forms.Form):
    payment_method = forms.ChoiceField(choices=PAYMENT_CHOICES)
    installment_period = forms.ChoiceField(choices=INSTALLMENT_CHOICES, required=False)
    # payment_store = forms.ChoiceField(choices=get_stores_choices, required=False)
    bank_name = forms.ChoiceField(choices=BANK_CHOICES, required=False)
    

class ShippingAddressSelectForm(forms.Form):
    ADDRESS_CHOICES = [
        (-1, 'Add new')
    ]

    addressSelected = forms.ChoiceField(widget=forms.RadioSelect, choices=ADDRESS_CHOICES, label='')


class PaymentStoreSelectForm(forms.Form):
    paymentStore = forms.ChoiceField(widget=forms.RadioSelect, choices=get_stores_choices, required=False, label='')


class StaffOrderCreateForm(forms.Form):
    orderChannel = forms.ChoiceField(widget=forms.Select, choices=ORDER_CHANNEL_CHOICES, label='Order channel')
    shippingCost = forms.IntegerField(required=False)
    notes = forms.CharField(widget=forms.Textarea, required=False)