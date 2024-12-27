# from trackerproject.app1.models import Expense, Income
# from trackerproject.app1.views import ExpenseFilter, IncomeFilter


# class FinancialSummaryFilterView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, *args, **kwargs):
#         # Fetch filters for income and expense
#         income_filter = IncomeFilter(request.query_params, queryset=Income.objects.all())
#         expense_filter = ExpenseFilter(request.query_params, queryset=Expense.objects.all())

#         # Apply sorting
#         sort_by = request.query_params.get('sort_by', 'date')  # Default to 'date'
#         order = request.query_params.get('order', 'asc')  # Default to ascending order

#         # Validate sorting order
#         if order not in ['asc', 'desc']:
#             return Response({"error": "Invalid order parameter. Use 'asc' or 'desc'."}, status=status.HTTP_400_BAD_REQUEST)

#         sort_order = '' if order == 'asc' else '-'
#         sorted_income = income_filter.qs.order_by(f"{sort_order}{sort_by}")
#         sorted_expense = expense_filter.qs.order_by(f"{sort_order}{sort_by}")

#         # Serialize data
#         income_data = IncomeSerializer(sorted_income, many=True).data
#         expense_data = ExpenseSerializer(sorted_expense, many=True).data

#         # Prepare response
#         response_data = {
#             "income_data": income_data,
#             "expense_data": expense_data,
#         }

#         return Response(response_data, status=status.HTTP_200_OK)