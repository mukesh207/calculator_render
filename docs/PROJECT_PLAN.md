# Django Calculator Project Plan

## Project Overview
A modern calculator web application built with Django and HTMX for seamless, dynamic interactions without full page reloads.

## Tech Stack
- **Backend**: Django 5.x
- **Frontend**: Django Templates + HTMX
- **Styling**: CSS3 (Custom modern UI)
- **Database**: SQLite (default) - for history tracking
- **Additional**: django-htmx library

## Project Structure
```
calculator_project/
├── manage.py
├── requirements.txt
├── calculator_site/          # Main project directory
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── calculator_app/           # Calculator application
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py             # Calculation history
    ├── views.py              # HTMX endpoints
    ├── urls.py
    ├── forms.py
    ├── migrations/
    ├── templates/
    │   └── calculator/
    │       ├── base.html
    │       ├── calculator.html
    │       ├── display.html  # HTMX partial
    │       └── history.html  # HTMX partial
    └── static/
        ├── css/
        │   └── calculator.css
        └── js/
            └── calculator.js  # Optional enhancements
```

## Features

### Core Features
1. **Basic Operations**: Addition, Subtraction, Multiplication, Division
2. **Advanced Operations**: Percentage, Square root, Power
3. **UI Features**:
   - Real-time display updates (HTMX)
   - Clear/All Clear functionality
   - Keyboard support
   - Responsive design (mobile-friendly)
4. **History Tracking**:
   - Save calculations to database
   - Display recent history
   - Clear history option

### HTMX Integration Points
- `hx-post`: Submit calculations without page reload
- `hx-target`: Update display area dynamically
- `hx-swap`: Replace/append content smoothly
- `hx-trigger`: Respond to button clicks and keyboard events

## Database Schema

### CalculationHistory Model
```python
- id: AutoField (primary key)
- expression: CharField(max_length=255)
- result: CharField(max_length=100)
- created_at: DateTimeField(auto_now_add=True)
- session_key: CharField (optional, for tracking user sessions)
```

## URL Routes

```python
/                          # Main calculator page
/calculate/                # HTMX POST endpoint for calculations
/history/                  # HTMX GET endpoint for history
/history/clear/            # Clear calculation history
```

## Views Architecture

### Main Views
1. **calculator_view**: Render main calculator page
2. **calculate_view**: Process calculation (HTMX endpoint)
3. **history_view**: Return history HTML fragment
4. **clear_history_view**: Clear user history

## UI Design Concept

### Layout
- **Display Area**: Large, clear readout for current input/result
- **Button Grid**: 4x5 or 4x6 grid layout
- **History Panel**: Collapsible sidebar or bottom panel
- **Color Scheme**: Modern gradient (e.g., dark theme with accent colors)

### Button Layout (4x5 Grid)
```
[AC] [DEL] [%]  [÷]
[7]  [8]   [9]  [×]
[4]  [5]   [6]  [-]
[1]  [2]   [3]  [+]
[0]  [.]   [√]  [=]
```

## Implementation Steps

### Phase 1: Project Setup
1. Create Django project and app
2. Install dependencies (django, django-htmx)
3. Configure settings.py
4. Create database models

### Phase 2: Backend Development
1. Implement models for calculation history
2. Create view functions with HTMX support
3. Setup URL routing
4. Add calculation logic with error handling

### Phase 3: Frontend Development
1. Design base template with HTMX library
2. Create calculator interface
3. Style with modern CSS (gradients, shadows, animations)
4. Add HTMX attributes for dynamic interactions

### Phase 4: Integration & Testing
1. Test all calculations
2. Test HTMX interactions
3. Validate error handling
4. Mobile responsiveness testing

### Phase 5: Enhancements (Optional)
1. Add themes (light/dark mode)
2. Scientific calculator mode
3. Export history as CSV
4. Keyboard shortcuts guide

## Key Files Content Preview

### requirements.txt
```
Django>=5.0
django-htmx>=1.17.0
```

### calculator_app/views.py (Simplified)
```python
from django.shortcuts import render
from django_htmx.middleware import HtmxDetails
from .models import CalculationHistory
import re

def calculator_view(request):
    return render(request, 'calculator/calculator.html')

def calculate_view(request):
    if request.htmx:
        expression = request.POST.get('expression', '')
        try:
            result = eval_safe(expression)
            CalculationHistory.objects.create(
                expression=expression,
                result=result
            )
            return render(request, 'calculator/display.html', {
                'result': result
            })
        except:
            return render(request, 'calculator/display.html', {
                'error': 'Error'
            })
```

### HTMX Template Example
```html
<button 
    hx-post="/calculate/" 
    hx-target="#display"
    hx-swap="innerHTML"
    class="calc-btn number">7</button>
```

## Security Considerations
1. Use safe evaluation methods (avoid direct `eval()`)
2. Validate all input expressions
3. Limit calculation complexity
4. Rate limiting for API endpoints
5. CSRF protection (Django default)

## Performance Optimizations
1. Cache recent calculations
2. Limit history records (e.g., last 50)
3. Use database indexing for session queries
4. Minimize HTMX payload sizes

## Testing Strategy
1. Unit tests for calculation logic
2. Integration tests for HTMX endpoints
3. UI testing for button interactions
4. Edge cases: division by zero, invalid input

## Deployment Considerations
- Collect static files
- Configure production settings
- Setup proper database (PostgreSQL for production)
- Configure ALLOWED_HOSTS
- Use environment variables for secrets

## Future Enhancements
- Unit conversion
- Graph plotting
- Complex number support
- Memory functions (M+, M-, MR, MC)
- User accounts for persistent history
- Share calculations via URL

## Timeline Estimate
- Setup & Backend: 2-3 hours
- Frontend & Styling: 3-4 hours
- Testing & Refinement: 1-2 hours
- **Total**: 6-9 hours for complete implementation
