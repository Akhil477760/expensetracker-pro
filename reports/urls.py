from django.urls import path
from .views import MonthlySummaryView, CategoryBreakdownView, AIInsightView

urlpatterns = [
    path('monthly-summary/', MonthlySummaryView.as_view(), name='monthly-summary'),
    path('category-breakdown/', CategoryBreakdownView.as_view(), name='category-breakdown'),
    path('ai-insight/', AIInsightView.as_view(), name='ai-insight'),
]