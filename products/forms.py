from django import forms
from .models import Product, ProductAttribute

class ProductAdjustStock(forms.Form):
    adjustmentType = forms.ChoiceField(choices=[
        ('purchase', 'Stock Purchasing'),
        ('refund', 'Refund to Supplier'),
        ('manual', 'Manual Adjustment')]
        , label='Adjustment Type')
    addSubtract = forms.ChoiceField(choices=[('Add', 'Add'),
                                    ('Subtract', 'Subtract')]
                                    , label='Add / Subtract')
    amount = forms.IntegerField(min_value=0)   #todo check if stock is higher when selected subtract
    purchasePrice = forms.IntegerField(min_value=0, required=False, label='Purchasing price per unit')
    comment = forms.CharField(max_length=100, required=False)


class ProductCreateForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = [
            'name',
            'categories',
            'price',
            'bottomPrice',
            'purchasePrice', 
            'description',
            'isFeatured',
            'isVisible',
            'purchaseOnlyViaEnquiry',
            'quantity',  
            'stockThreshold',
            # 'latestPurchasingPrice'
            'seoMetaTags',
            'relatedCarBrand',
            'featured_image'
        ]


class ProductFullForm(ProductCreateForm):   # extending the Product Create form to add the images to the form
    # featured_image = forms.ImageField()
    gallery_images = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': True}), help_text='Recommended image dimentions are 300 x 300 pixel')

    class Meta(ProductCreateForm.Meta):
        fields = ProductCreateForm.Meta.fields + ['gallery_images']


#? form got depricated due to the class based view in views. Delete once going in production..
# class ProductEditForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = [
#             'name',
#             'description',
#             'price',
#             'purchaseOnlyViaEnquiry',
#             # 'latestPurchasingPrice'
#             'bottomPrice',
#             'stockThreshold',

#             # 'quantity',  
#             # 'purchasePrice', 

#             'seoMetaTags',
#             'isVisible',
#             'isFeatured',
#             'categories',
#             'relatedCarBrand',
#         ]


class ProductAttributeCreateForm(forms.ModelForm):
    class Meta:
        model = ProductAttribute
        fields = [
            'attribute',
            'values'
        ]