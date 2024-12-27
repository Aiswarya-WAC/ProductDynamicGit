

from django.urls import path
from .views import ExpenseCreate, ExpenseUpdate, FinancialSummaryFilterView, FinancialSummarySortView, IncomeCreate, IncomeUpdate, RegisterView, LoginView, FinancialSummaryView

urlpatterns = [
    # User authentication views
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),

    # Expense and Income creation views
    path('expense/', ExpenseCreate.as_view(), name='expense-create'),
    path('income/', IncomeCreate.as_view(), name='income-create'),

    # Expense and Income update views
    path('expense_edit/<int:pk>/', ExpenseUpdate.as_view(), name='expense-update'),
    path('income_edit/<int:pk>/', IncomeUpdate.as_view(), name='income-update'),

    # Financial summary view for combined expense and income data
    path('financial-summary/', FinancialSummaryView.as_view(), name='financial-summary'),
    path('financial-summary/filter/', FinancialSummaryFilterView.as_view(), name='financial-summary-filter'),
    path('financial-summary/sort/', FinancialSummarySortView.as_view(), name='financial-summary-sort')
]

