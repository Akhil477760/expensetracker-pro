from django.conf import settings
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from transactions.models import Transaction


class MonthlySummaryView(APIView):
    """
    GET /api/reports/monthly-summary/?month=7&year=2026
    Returns total income, total expense, and net savings for the month.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        month = request.query_params.get('month')
        year = request.query_params.get('year')
        qs = Transaction.objects.filter(user=request.user)
        if month and year:
            qs = qs.filter(date__month=month, date__year=year)

        income = qs.filter(type='income').aggregate(total=Sum('amount'))['total'] or 0
        expense = qs.filter(type='expense').aggregate(total=Sum('amount'))['total'] or 0

        return Response({
            'month': month,
            'year': year,
            'total_income': income,
            'total_expense': expense,
            'net_savings': float(income) - float(expense),
        })


class CategoryBreakdownView(APIView):
    """
    GET /api/reports/category-breakdown/?month=7&year=2026&type=expense
    Returns spend/income grouped by category - perfect for a pie chart.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        month = request.query_params.get('month')
        year = request.query_params.get('year')
        txn_type = request.query_params.get('type', 'expense')

        qs = Transaction.objects.filter(user=request.user, type=txn_type)
        if month and year:
            qs = qs.filter(date__month=month, date__year=year)

        breakdown = (
            qs.values('category__name')
            .annotate(total=Sum('amount'))
            .order_by('-total')
        )
        return Response(list(breakdown))


class AIInsightView(APIView):
    """
    GET /api/reports/ai-insight/?month=7&year=2026
    Sends the month's category breakdown to Gemini and returns a short,
    plain-language savings tip.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if not settings.GEMINI_API_KEY:
            return Response(
                {'error': 'GEMINI_API_KEY not configured. Add it to your .env file.'},
                status=400
            )

        month = request.query_params.get('month')
        year = request.query_params.get('year')
        qs = Transaction.objects.filter(user=request.user, type='expense')
        if month and year:
            qs = qs.filter(date__month=month, date__year=year)

        breakdown = list(
            qs.values('category__name').annotate(total=Sum('amount')).order_by('-total')
        )

        if not breakdown:
            return Response({'insight': 'No expense data yet for this period.'})

        try:
            import google.generativeai as genai
            genai.configure(api_key=settings.GEMINI_API_KEY)
            model = genai.GenerativeModel('gemini-3.1-flash-lite')

            spend_summary = ", ".join(
                f"{item['category__name']}: Rs.{item['total']}" for item in breakdown
            )
            prompt = (
                f"Here is a user's monthly spending by category: {spend_summary}. "
                "In 2-3 short sentences, give one practical savings tip based on "
                "where they are spending the most. Keep it friendly and specific."
            )
            response = model.generate_content(prompt)
            return Response({'insight': response.text})
        except Exception as e:
            return Response({'error': f'AI request failed: {str(e)}'}, status=500)