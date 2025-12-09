from django.contrib import admin
from .models import CalculationHistory

@admin.register(CalculationHistory)
class CalculationHistoryAdmin(admin.ModelAdmin):
    list_display = ('expression', 'result', 'created_at', 'session_key')
    list_filter = ('created_at',)
    search_fields = ('expression', 'result')
