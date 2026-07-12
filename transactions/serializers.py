from rest_framework import serializers
from .models import Category, Transaction


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'type', 'created_at')
        read_only_fields = ('id', 'created_at')


class TransactionSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Transaction
        fields = (
            'id', 'category', 'category_name', 'amount', 'type',
            'date', 'note', 'payment_method', 'is_recurring', 'created_at'
        )
        read_only_fields = ('id', 'created_at')

    def validate(self, attrs):
        category = attrs.get('category')
        txn_type = attrs.get('type')
        if category and txn_type and category.type != txn_type:
            raise serializers.ValidationError(
                "Category type must match transaction type (income/expense)."
            )
        return attrs