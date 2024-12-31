from django.contrib import admin

from app1.models import Attribute, Category, Product, SubAttribute, SubCategory

# Register your models here.

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Attribute)
admin.site.register(SubAttribute)

