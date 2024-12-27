from django.contrib.auth import authenticate
from .models import Expense
from .models import Income
from django.contrib.auth.models import User
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializer import ExpenseSerializer, IncomeSerializer, RegisterSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from django.db.models import Sum
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Expense, Income
from .serializer import ExpenseSerializer, IncomeSerializer
from rest_framework import serializers
import django_filters
from django_filters import rest_framework as filters


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        print("req=" ,request)

        user = authenticate(username=username, password=password)
        print("user=",user)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            })
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)



class ExpenseUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

class IncomeUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer

class ExpenseCreate(APIView):
    permission_classes = [IsAuthenticated] 

    def post(self, request, *args, **kwargs):
        print(request)
        serializer = ExpenseSerializer(data=request.data)

        if serializer.is_valid():
            print("serilaizer=", serializer.validated_data)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IncomeCreate(APIView):
    permission_classes = [IsAuthenticated]  

    def post(self, request, *args, **kwargs):
        print(request)
        serializer = IncomeSerializer(data=request.data)
      

        if serializer.is_valid():
            print("serilaizer=", serializer.validated_data)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# Create a Filter for Expense and Income
class ExpenseFilter(filters.FilterSet):
    category = filters.CharFilter(field_name='category', lookup_expr='icontains')
    description = filters.CharFilter(field_name='description', lookup_expr='icontains')
    amount = filters.NumberFilter(field_name='amount')
    date = filters.DateFilter(field_name='date')

    class Meta:
        model = Expense
        fields = ['category', 'description', 'amount', 'date']


class IncomeFilter(filters.FilterSet):
    category = filters.CharFilter(field_name='category', lookup_expr='icontains')
    description = filters.CharFilter(field_name='description', lookup_expr='icontains')
    amount = filters.NumberFilter(field_name='amount')
    date = filters.DateFilter(field_name='date')

    class Meta:
        model = Income
        fields = ['category', 'description', 'amount', 'date']


class FinancialSummaryView(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request, *args, **kwargs):
        # Fetch all income and expense records, with optional filters
        income_filter = IncomeFilter(request.query_params, queryset=Income.objects.all())
        expense_filter = ExpenseFilter(request.query_params, queryset=Expense.objects.all())

        total_income = income_filter.qs.aggregate(Sum('amount'))['amount__sum'] or 0
        total_expenses = expense_filter.qs.aggregate(Sum('amount'))['amount__sum'] or 0
        overall_balance = total_income - total_expenses

        # Prepare data to return in response
        response_data = {
            "total_income": total_income,
            "total_expenses": total_expenses,
            "overall_balance": overall_balance,
            "income_data": IncomeSerializer(income_filter.qs, many=True).data,
            "expense_data": ExpenseSerializer(expense_filter.qs, many=True).data
        }
        
        
        return Response(response_data, status=status.HTTP_200_OK)    
    
class FinancialSummaryFilterView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Apply filters to Income and Expense
        income_filter = IncomeFilter(request.query_params, queryset=Income.objects.all())
        expense_filter = ExpenseFilter(request.query_params, queryset=Expense.objects.all())

        # Filtered data
        filtered_income = income_filter.qs
        filtered_expense = expense_filter.qs

        # Prepare response data
        response_data = {
            "income_data": IncomeSerializer(filtered_income, many=True).data,
            "expense_data": ExpenseSerializer(filtered_expense, many=True).data,
        }

        return Response(response_data, status=200)
class FinancialSummarySortView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Fetch filters for income and expense
        income_filter = IncomeFilter(request.query_params, queryset=Income.objects.all())
        expense_filter = ExpenseFilter(request.query_params, queryset=Expense.objects.all())

        # Get sorting parameters
        sort_by = request.query_params.get('sort_by', 'date')  # Default to 'date'
        order = request.query_params.get('order', 'asc')  # Default to ascending order

        # Debug query params
        print(f"Sorting by: {sort_by}, Order: {order}")

        # Validate sorting order
        if order not in ['asc', 'desc']:
            return Response({"error": "Invalid order parameter. Use 'asc' or 'desc'."}, status=status.HTTP_400_BAD_REQUEST)

        # Validate sort_by field
        valid_sort_fields = ['date', 'category', 'amount', 'description']
        if sort_by not in valid_sort_fields:
            return Response({"error": f"Invalid sort_by field. Choose from {', '.join(valid_sort_fields)}."}, status=status.HTTP_400_BAD_REQUEST)

        # Determine the sorting order
        sort_order = '' if order == 'asc' else '-'

        # Apply sorting to both income and expense filters
        sorted_income = income_filter.qs.order_by(f"{sort_order}{sort_by}")
        sorted_expense = expense_filter.qs.order_by(f"{sort_order}{sort_by}")

        # Debug the actual query being executed
        print(f"Sorted Income Query: {sorted_income.query}")
        print(f"Sorted Expense Query: {sorted_expense.query}")

        # Serialize data
        income_data = IncomeSerializer(sorted_income, many=True).data
        expense_data = ExpenseSerializer(sorted_expense, many=True).data

        # Prepare response
        response_data = {
            "income_data": income_data,
            "expense_data": expense_data,
        }

        return Response(response_data, status=status.HTTP_200_OK)