from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    category = models.ForeignKey(Category, related_name="subcategories", on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, related_name="subcategories", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} ({'Main' if not self.parent else 'Subcategory'})"

class Attribute(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class SubAttribute(models.Model):
    attribute = models.ForeignKey(Attribute, related_name="subattributes", on_delete=models.CASCADE)
    value = models.CharField(max_length=255)

    def __str__(self):
        return self.value

class Product(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='products/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, related_name="products", on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, related_name="products", on_delete=models.CASCADE)
    attributes = models.ManyToManyField(Attribute, related_name="products")
    subattributes = models.ManyToManyField(SubAttribute, related_name="products")

    def __str__(self):
        return self.name
