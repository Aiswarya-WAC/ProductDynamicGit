from django.db import models

    
class Expense(models.Model):
    
    description = models.CharField(max_length=50)
    category = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    def __str__(self):
            return f"{self.transaction_type} - {self.category} - {self.amount} on {self.date}"
    
class Income(models.Model):
    
    description = models.CharField(max_length=50)
    category = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    def __str__(self):
            return f"{self.transaction_type} - {self.category} - {self.amount} on {self.date}"