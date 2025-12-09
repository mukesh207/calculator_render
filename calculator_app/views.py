from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from .models import CalculationHistory
import re

def calculator_view(request):
    """Main calculator page"""
    recent_history = CalculationHistory.objects.filter(
        session_key=request.session.session_key
    )[:10] if request.session.session_key else []
    
    return render(request, 'calculator/calculator.html', {
        'history': recent_history
    })

def safe_eval(expression):
    """Safely evaluate mathematical expressions"""
    expression = expression.replace(' ', '')
    expression = expression.replace('×', '*').replace('÷', '/')
    
    if not re.match(r'^[\d+\-*/.()%√^]+$', expression):
        raise ValueError("Invalid characters in expression")
    
    expression = re.sub(r'(\d+)%', r'(\1/100)', expression)
    expression = expression.replace('√', 'sqrt')
    
    if len(expression) > 100:
        raise ValueError("Expression too long")
    
    safe_dict = {
        '__builtins__': {},
        'sqrt': lambda x: x ** 0.5,
    }
    
    try:
        result = eval(expression, safe_dict)
        if isinstance(result, float):
            result = round(result, 10)
        return str(result)
    except Exception as e:
        raise ValueError(f"Calculation error: {str(e)}")

@require_http_methods(["POST"])
def calculate_view(request):
    """HTMX endpoint for calculations"""
    if not request.htmx:
        return HttpResponse("Bad Request", status=400)
    
    expression = request.POST.get('expression', '')
    
    if not expression:
        return render(request, 'calculator/display.html', {
            'display': '0',
            'expression': ''
        })
    
    try:
        result = safe_eval(expression)
        
        if not request.session.session_key:
            request.session.create()
        
        CalculationHistory.objects.create(
            expression=expression,
            result=result,
            session_key=request.session.session_key
        )
        
        return render(request, 'calculator/display.html', {
            'display': result,
            'expression': expression
        })
    except Exception as e:
        return render(request, 'calculator/display.html', {
            'display': 'Error',
            'expression': expression,
            'error': True
        })

def history_view(request):
    """HTMX endpoint for history"""
    if not request.htmx:
        return HttpResponse("Bad Request", status=400)
    
    history = CalculationHistory.objects.filter(
        session_key=request.session.session_key
    )[:20] if request.session.session_key else []
    
    return render(request, 'calculator/history.html', {
        'history': history
    })

@require_http_methods(["POST"])
def clear_history_view(request):
    """Clear calculation history"""
    if request.session.session_key:
        CalculationHistory.objects.filter(
            session_key=request.session.session_key
        ).delete()
    
    if request.htmx:
        return render(request, 'calculator/history.html', {
            'history': []
        })
    
    return HttpResponse("History cleared")
