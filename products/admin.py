from django.contrib import admin
from .models import (
    Attribute, 
    Category, 
    Product, 
    ProductImage,
    ProductAttribute
)
from orders.models import ProductHistory
from .models import ProductSearchQuery

# adding additional fields to the admin tables
class ProductAdmin(admin.ModelAdmin):
    date_hierarchy = 'dateCreated'
    search_fields = ['name', 'description']
    list_display = ['dateCreated', 'name', 'price', 'slug']
    # list_editable = ['slug']
    # list_filter = ['price']   # creates a filter of products
    readonly_fields = ['dateCreated', 'dateEdited'] # shows these fields only as read only in the profile itself
    prepopulated_fields = {"slug": ("name",)}

    class Meta:
        model = Product

class ProductHistoryAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'adjustmentType', 'newQuantity', 'product']
    class Meta:
        model = Product

class ProductSearchQueryAdmin(admin.ModelAdmin):
    list_display = ['timestampCreated', 'queryData']
    class Meta:
        model = ProductSearchQuery

admin.site.register(Attribute)
admin.site.register(ProductSearchQuery, ProductSearchQueryAdmin)
admin.site.register(ProductAttribute)
admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(ProductHistory, ProductHistoryAdmin)