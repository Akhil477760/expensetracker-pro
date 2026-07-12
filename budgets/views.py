from rest_framework import viewsets, permissions
from .models import Budget
from .serializers import BudgetSerializer


class BudgetViewSet(viewsets.ModelViewSet):
    """
    /api/budgets/               GET (list), POST (create)
    /api/budgets/<id>/          GET, PATCH, DELETE
    Each budget response includes 'spent' and 'percentage_used' automatically.
    """
    serializer_class = BudgetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)