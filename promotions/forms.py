from django import forms
from .models import Promotion

class PromotionCreateForm(forms.ModelForm):
    class Meta:
        model = Promotion
        fields = "__all__"
        widgets = {
            'dateStart': forms.widgets.DateInput(attrs={'type': 'date'}),
            'dateEnd': forms.widgets.DateInput(attrs={'type': 'date'}),
        }

class PromotionEditForm(forms.ModelForm):
    class Meta:
        model = Promotion
        fields = "__all__"
        widgets = {
            'dateStart': forms.widgets.DateInput(attrs={'type': 'date'}),
            'dateEnd': forms.widgets.DateInput(attrs={'type': 'date'}),
        }
