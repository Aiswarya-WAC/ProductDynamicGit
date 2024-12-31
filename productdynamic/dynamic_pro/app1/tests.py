from django.test import TestCase

# Create your tests here.
from rest_framework import serializers
from .models import Category, SubCategory, Product, Attribute, SubAttribute

class SubAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubAttribute
        fields = ['id', 'value']

class AttributeSerializer(serializers.ModelSerializer):
    subattributes = SubAttributeSerializer(many=True)

    class Meta:
        model = Attribute
        fields = ['id', 'name', 'subattributes']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class SubCategorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    class Meta:
        model = SubCategory
        fields = ['id', 'name','category_name','parent']
        #depth = 2 

class ProductSerializer(serializers.ModelSerializer):
    attributes = AttributeSerializer(many=True)
    subattributes = SubAttributeSerializer(many=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'image', 'price', 'category', 'subcategory', 'attributes', 'subattributes']
