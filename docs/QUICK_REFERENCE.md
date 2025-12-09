# Quick Reference Guide

## File Structure Created

```
calculator_project/
├── README.md                          # Project overview
├── PROJECT_PLAN.md                    # Detailed architecture plan
├── IMPLEMENTATION_GUIDE.md            # Step-by-step setup guide
├── requirements.txt                   # Python dependencies
│
├── calculator_app/
│   ├── templates/calculator/
│   │   ├── base.html                 # Base template with HTMX
│   │   ├── calculator.html           # Main calculator interface
│   │   ├── display.html              # Display partial (HTMX target)
│   │   └── history.html              # History partial (HTMX target)
│   │
│   └── static/css/
│       └── calculator.css            # Complete styling
│
└── docs/
    └── QUICK_REFERENCE.md            # This file
```

## Next Steps to Get Running

### 1. Initialize Django Project
```bash
cd calculator_project
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
django-admin startproject calculator_site .
python manage.py startapp calculator_app
```

### 2. Copy Files to Django App
The templates and static files are already in the right location!

### 3. Create Essential Files

**models.py** (in calculator_app/):
```python
from django.db import models

class CalculationHistory(models.Model):
    expression = models.CharField(max_length=255)
    result = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    session_key = models.CharField(max_length=40, blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.expression} = {self.result}"
```

**views.py** - See IMPLEMENTATION_GUIDE.md for complete code

**urls.py** - See IMPLEMENTATION_GUIDE.md for complete code

### 4. Update Settings
Add to `calculator_site/settings.py`:
- 'django_htmx' to INSTALLED_APPS
- 'calculator_app' to INSTALLED_APPS  
- 'django_htmx.middleware.HtmxMiddleware' to MIDDLEWARE

### 5. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Start Server
```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000/

## Key Features Implemented

### HTMX Integration
- **Calculate**: POST to `/calculate/` updates display without reload
- **History**: GET from `/history/` loads calculation history
- **Clear History**: POST to `/history/clear/` clears records

### UI Components
- **Display Area**: Shows current expression and result
- **Button Grid**: 4x5 grid with numbers, operators, and functions
- **History Panel**: Side panel showing recent calculations
- **Responsive**: Works on mobile and desktop

### JavaScript Functions
- `appendValue(val)`: Add digit/operator to expression
- `deleteLast()`: Remove last character
- `clearAll()`: Reset calculator
- `calculate()`: Submit calculation via HTMX
- Keyboard support for all operations

### Styling Features
- Dark theme with gradient background
- Smooth animations and transitions
- Hover effects on buttons
- Responsive grid layout
- Custom scrollbar for history

## HTMX Patterns Used

### 1. Form Submission
```html
<form hx-post="/calculate/" hx-target="#display" hx-swap="innerHTML">
```

### 2. Button Actions
```html
<button hx-get="/history/" hx-target="#history-panel">
```

### 3. Confirmation
```html
<button hx-confirm="Clear all history?">
```

### 4. Response Handling
```javascript
document.body.addEventListener('htmx:afterSwap', function(event) {
    // Handle response
});
```

## Testing Scenarios

1. **Basic Math**: 7 + 3 = 10
2. **Chain Operations**: 5 × 3 + 2 = 17
3. **Decimals**: 3.14 × 2 = 6.28
4. **Division by Zero**: Should show Error
5. **Keyboard Input**: Type numbers and operators
6. **History**: View past calculations
7. **Clear**: AC button resets display

## Customization Options

### Change Theme Colors
Edit CSS variables in `calculator.css`:
```css
:root {
    --primary-bg: #1a1a2e;        /* Background */
    --highlight-color: #e94560;    /* Accent */
    --btn-number: #2d3561;         /* Number buttons */
}
```

### Add More Operations
1. Add button in `calculator.html`
2. Add operation to `safe_eval()` in `views.py`
3. Style in `calculator.css`

### Modify History Limit
In `views.py`, change `[:20]` to desired number:
```python
history = CalculationHistory.objects.filter(...)[:50]
```

## Common Issues & Solutions

### HTMX Not Working
- Check if HTMX script is loaded in base.html
- Verify django_htmx middleware is installed
- Check browser console for errors

### Static Files Not Loading
```bash
python manage.py collectstatic
# Add to settings.py:
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'calculator_app/static']
```

### CSRF Errors
- Ensure {% csrf_token %} is in forms
- Check CSRF middleware is enabled

### History Not Showing
- Run migrations to create database tables
- Check session is being created
- Verify session middleware is enabled

## Production Deployment

1. Set `DEBUG = False` in settings
2. Configure `ALLOWED_HOSTS`
3. Use PostgreSQL instead of SQLite
4. Setup static files serving (WhiteNoise or CDN)
5. Enable security settings (HTTPS, CSP, etc.)
6. Use environment variables for secrets

## Resources

- Django Docs: https://docs.djangoproject.com/
- HTMX Docs: https://htmx.org/docs/
- django-htmx: https://github.com/adamchainz/django-htmx

## Support

For issues with this project structure:
1. Check IMPLEMENTATION_GUIDE.md for detailed setup
2. Review PROJECT_PLAN.md for architecture details
3. Verify all files are in correct locations
4. Check Django and HTMX are properly installed
