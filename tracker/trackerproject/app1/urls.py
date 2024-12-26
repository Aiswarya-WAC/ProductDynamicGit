from django.urls import path
from .views import ExpenseCreate, ExpenseUpdate, IncomeCreate, IncomeUpdate, RegisterView, LoginView    

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('expense/', ExpenseCreate.as_view(), name='expense-create'),
    path('income/', IncomeCreate.as_view(), name='income-create'),
    path('expense_edit/<int:pk>/', ExpenseUpdate.as_view(), name='texpense-update'),
    path('income_edit/<int:pk>/', IncomeUpdate.as_view(), name='income-update'),
]
