from rest_framework import serializers
from django.db.models import Sum
from transactions.models import Transaction
from .models import Budget


class BudgetSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    spent = serializers.SerializerMethodField()
    percentage_used = serializers.SerializerMethodField()

    class Meta:
        model = Budget
        fields = (
            'id', 'category', 'category_name', 'month', 'year',
            'limit_amount', 'spent', 'percentage_used', 'created_at'
        )
        read_only_fields = ('id', 'created_at')

    def get_spent(self, obj):
        total = Transaction.objects.filter(
            user=obj.user, category=obj.category, type='expense',
            date__month=obj.month, date__year=obj.year
        ).aggregate(total=Sum('amount'))['total']
        return total or 0

    def get_percentage_used(self, obj):
        spent = self.get_spent(obj)
        if obj.limit_amount and obj.limit_amount > 0:
            return round((float(spent) / float(obj.limit_amount)) * 100, 1)
        return 0