from rest_framework import serializers
from products.models import Product, ProductAttribute

class ProductSearchSerializer(serializers.Serializer):
    name = serializers.CharField(allow_blank=True, max_length=100)
    attribute = serializers.CharField(allow_blank=True, max_length=100)
    attributeValue = serializers.CharField(allow_blank=True, max_length=100)
    brand = serializers.CharField(allow_blank=True, max_length=100)
    category = serializers.CharField(allow_blank=True, max_length=100)


class ProductAttributesSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductAttribute
        fields = [
            'attribute',
            'values'
        ]

# todo convert this to HyperlinkedModelSerializer to be able to view product attributes as well..
class ProductSerializer(serializers.ModelSerializer):
    productattribute = ProductAttributesSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
        'id',
        'name', 
        'quantity', 
        'categories',
        'productattribute',
        'bottomPrice', 
        'price',
        'sku',
        ]
        depth = 1


class UpdateCartSerializer(serializers.Serializer):
    userId = serializers.IntegerField(required=False)
    productId = serializers.IntegerField()
    quantity = serializers.IntegerField()
