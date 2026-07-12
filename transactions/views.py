from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend

from .models import Category, Transaction
from .serializers import CategorySerializer, TransactionSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
    /api/categories/       GET (list), POST (create)
    /api/categories/<id>/  GET, PATCH, DELETE
    """
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Users only ever see their own categories
        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TransactionViewSet(viewsets.ModelViewSet):
    """
    /api/transactions/                         GET (list, supports filters), POST (create)
    /api/transactions/<id>/                    GET, PATCH, DELETE
    Filters: ?type=expense&category=<id>&date=2026-07-01
    """
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['type', 'category', 'date', 'is_recurring']

    def get_queryset(self):
        queryset = Transaction.objects.filter(user=self.request.user)
        month = self.request.query_params.get('month')
        year = self.request.query_params.get('year')
        if month and year:
            queryset = queryset.filter(date__month=month, date__year=year)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)