# Implementation Guide

## Step-by-Step Implementation

### Step 1: Initialize Django Project

```bash
cd calculator_project
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
django-admin startproject calculator_site .
python manage.py startapp calculator_app
```

### Step 2: Configure Settings

Add to `calculator_site/settings.py`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_htmx',  # Add this
    'calculator_app',  # Add this
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_htmx.middleware.HtmxMiddleware',  # Add this
]
```

### Step 3: Create Models

`calculator_app/models.py`:

```python
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
```

### Step 4: Create Views

`calculator_app/views.py`:

```python
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from .models import CalculationHistory
import re
import operator

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
    # Remove spaces
    expression = expression.replace(' ', '')
    
    # Replace visual operators with Python operators
    expression = expression.replace('×', '*').replace('÷', '/')
    
    # Validate expression contains only allowed characters
    if not re.match(r'^[\d+\-*/.()%√^]+$', expression):
        raise ValueError("Invalid characters in expression")
    
    # Handle percentage
    expression = re.sub(r'(\d+)%', r'(\1/100)', expression)
    
    # Handle square root
    expression = expression.replace('√', 'sqrt')
    
    # Limit expression length
    if len(expression) > 100:
        raise ValueError("Expression too long")
    
    # Safe evaluation with limited namespace
    safe_dict = {
        '__builtins__': {},
        'sqrt': lambda x: x ** 0.5,
    }
    
    try:
        result = eval(expression, safe_dict)
        # Round to avoid floating point errors
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
        
        # Save to history
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
```

### Step 5: Setup URLs

`calculator_app/urls.py`:

```python
from django.urls import path
from . import views

app_name = 'calculator'

urlpatterns = [
    path('', views.calculator_view, name='home'),
    path('calculate/', views.calculate_view, name='calculate'),
    path('history/', views.history_view, name='history'),
    path('history/clear/', views.clear_history_view, name='clear_history'),
]
```

`calculator_site/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('calculator_app.urls')),
]
```

### Step 6: Create Templates

See separate files for:
- `templates/calculator/base.html`
- `templates/calculator/calculator.html`
- `templates/calculator/display.html`
- `templates/calculator/history.html`

### Step 7: Create CSS

See `static/css/calculator.css` for styling

### Step 8: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser  # Optional
```

### Step 9: Test

```bash
python manage.py runserver
```

## Testing Checklist

- [ ] Basic operations (+, -, ×, ÷)
- [ ] Decimal numbers
- [ ] Multiple operations in sequence
- [ ] Clear and All Clear
- [ ] History display
- [ ] Clear history
- [ ] Error handling (division by zero, invalid input)
- [ ] Mobile responsiveness
- [ ] Keyboard support

## Deployment Checklist

- [ ] Set DEBUG=False
- [ ] Configure ALLOWED_HOSTS
- [ ] Setup production database
- [ ] Collect static files
- [ ] Configure CSRF trusted origins
- [ ] Setup environment variables
- [ ] Enable security features
