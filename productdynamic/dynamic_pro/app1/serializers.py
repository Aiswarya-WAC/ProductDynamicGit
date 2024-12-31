from rest_framework import serializers
from .models import Category, SubCategory, Product, Attribute, SubAttribute
from rest_framework import serializers
from .models import Product, Attribute, SubAttribute

class SubCategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'category', 'parent', 'subcategories']

    def get_subcategories(self, obj):
        subcategories = obj.subcategories.all()
        return SubCategorySerializer(subcategories, many=True).data

class AttributeSerializer(serializers.ModelSerializer):
    subattributes = serializers.SerializerMethodField()

    class Meta:
        model = Attribute
        fields = ['id', 'name', 'subattributes']

    def get_subattributes(self, obj):
        subattributes = obj.subattributes.all()
        return SubAttributeSerializer(subattributes, many=True).data

class SubAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubAttribute
        fields = ['id', 'value','attribute']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']



class ProductSerializer(serializers.ModelSerializer):
    attributes = AttributeSerializer(many=True)
    subattributes = SubAttributeSerializer(many=True)

    class Meta:
        model = Product
        # Exclude the image field from serialization
        fields = ['id', 'name', 'price', 'category', 'subcategory', 'attributes', 'subattributes']

    def create(self, validated_data):
        # Extract the attributes and subattributes from the validated data
        attributes_data = validated_data.pop('attributes', [])
        subattributes_data = validated_data.pop('subattributes', [])

        # Create the product object without image
        product = Product.objects.create(**validated_data)

        # Create and associate the attributes with the product
        for attribute_data in attributes_data:
            attribute = Attribute.objects.create(**attribute_data)
            product.attributes.add(attribute)

        # Create and associate the subattributes with the product
        for subattribute_data in subattributes_data:
            subattribute = SubAttribute.objects.create(**subattribute_data)
            product.subattributes.add(subattribute)

        return product