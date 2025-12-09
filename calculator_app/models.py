from django.db import models

class CalculationHistory(models.Model):
    expression = models.CharField(max_length=255)
    result = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    session_key = models.CharField(max_length=40, blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Calculation Histories"
    
    def __str__(self):
        return f"{self.expression} = {self.result}"
