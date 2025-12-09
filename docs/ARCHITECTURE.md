# Django HTMX Calculator - Architecture Diagram

## 🏗️ Project Structure
```
calculator_project/
│
├── 📄 requirements.txt              # Django, django-htmx
├── 📘 README.md                     # Quick start guide
├── 📗 PROJECT_PLAN.md               # Full architecture details
├── 📙 IMPLEMENTATION_GUIDE.md       # Step-by-step setup
├── 📕 QUICK_REFERENCE.md            # Quick commands & tips
│
├── 🔧 calculator_site/              # Django project (to be created)
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
└── 🎯 calculator_app/               # Main application
    │
    ├── 🗄️ Database Layer
    │   └── models.py                # CalculationHistory model
    │
    ├── 🎮 Controller Layer
    │   ├── views.py                 # calculator_view, calculate_view, 
    │   │                            # history_view, clear_history_view
    │   └── urls.py                  # URL routing
    │
    ├── 🎨 View Layer (Templates)
    │   └── templates/calculator/
    │       ├── base.html            # Base with HTMX script
    │       ├── calculator.html      # Main interface + JS logic
    │       ├── display.html         # HTMX partial for display
    │       └── history.html         # HTMX partial for history list
    │
    └── 💅 Static Assets
        └── static/css/
            └── calculator.css       # Complete styling (dark theme)
```

## 🔄 Data Flow Architecture

```
User Action (Browser)
    ↓
┌─────────────────────────────────────────┐
│  Frontend (Django Templates + HTMX)     │
│  ┌──────────────────────────────────┐   │
│  │  Calculator Interface            │   │
│  │  - Display Area                  │   │
│  │  - Button Grid (4x5)            │   │
│  │  - JavaScript Event Handlers     │   │
│  └──────────────────────────────────┘   │
└─────────────────────────────────────────┘
    ↓ (HTMX POST/GET)
┌─────────────────────────────────────────┐
│  Django Backend (Views)                 │
│  ┌──────────────────────────────────┐   │
│  │  URL Router                      │   │
│  │  urls.py: /calculate/            │   │
│  └──────────────────────────────────┘   │
│    ↓                                     │
│  ┌──────────────────────────────────┐   │
│  │  View Functions                  │   │
│  │  - safe_eval() for security      │   │
│  │  - Expression validation         │   │
│  │  - Result calculation            │   │
│  └──────────────────────────────────┘   │
│    ↓                                     │
│  ┌──────────────────────────────────┐   │
│  │  Database Operations             │   │
│  │  - Save to CalculationHistory    │   │
│  │  - Query history by session      │   │
│  └──────────────────────────────────┘   │
└─────────────────────────────────────────┘
    ↓ (HTML Fragment Response)
┌─────────────────────────────────────────┐
│  HTMX Swap                              │
│  - Update #display-container            │
│  - Update #history-panel                │
└─────────────────────────────────────────┘
```

## 🎯 HTMX Interaction Flow

### Calculation Flow
```
1. User clicks button "7"
   → JavaScript: appendValue('7')
   → Updates display locally
   
2. User clicks button "+"
   → JavaScript: appendValue('+')
   → Updates expression
   
3. User clicks button "3"
   → JavaScript: appendValue('3')
   
4. User clicks "=" button
   → JavaScript: calculate()
   → Triggers HTMX form submission
   
5. HTMX sends POST to /calculate/
   → Includes: expression="7+3"
   
6. Django view processes:
   → Validates expression
   → Calculates result: 10
   → Saves to database
   → Returns display.html with result
   
7. HTMX receives HTML fragment
   → Swaps into #display-container
   → Shows result: 10
   
8. JavaScript afterSwap event
   → Refreshes history panel
```

### History Flow
```
1. User clicks history button 📊
   → HTMX GET /history/
   
2. Django queries database
   → Filter by session_key
   → Last 20 calculations
   
3. Django renders history.html
   → List of calculation items
   
4. HTMX swaps into #history-panel
   → Shows recent calculations
```

## 🎨 UI Component Layout

```
┌────────────────────────────────────────────────────────┐
│  Calculator                              [📊 History]  │
├────────────────────────────────────────────────────────┤
│                                                        │
│  Expression: 7 + 3                                    │
│  Display:    10                                       │
│                                                        │
├────────────────────────────────────────────────────────┤
│                                                        │
│  [AC]  [DEL]   [%]    [÷]                            │
│                                                        │
│  [ 7]  [ 8]   [ 9]    [×]                            │
│                                                        │
│  [ 4]  [ 5]   [ 6]    [-]                            │
│                                                        │
│  [ 1]  [ 2]   [ 3]    [+]                            │
│                                                        │
│  [    0    ]  [.]     [=]                            │
│                                                        │
└────────────────────────────────────────────────────────┘

┌───────────────────────┐
│  History    [Clear]   │
├───────────────────────┤
│                       │
│  7 + 3                │
│  = 10                 │
│  12:34:56             │
│  ─────────────────    │
│  5 × 2                │
│  = 10                 │
│  12:34:45             │
│  ─────────────────    │
│  ...                  │
│                       │
└───────────────────────┘
```

## 🔐 Security Architecture

```
User Input
    ↓
┌─────────────────────────────────┐
│  Input Validation               │
│  - Character whitelist          │
│  - Length limits                │
│  - Pattern matching             │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│  Safe Evaluation                │
│  - Restricted namespace         │
│  - No eval() of arbitrary code  │
│  - Operator normalization       │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│  Django Security                │
│  - CSRF protection              │
│  - SQL injection prevention     │
│  - XSS protection (templates)   │
└─────────────────────────────────┘
```

## 📊 Database Schema

```
┌────────────────────────────────┐
│  CalculationHistory            │
├────────────────────────────────┤
│  id: AutoField (PK)            │
│  expression: CharField(255)    │
│  result: CharField(100)        │
│  created_at: DateTimeField     │
│  session_key: CharField(40)    │
└────────────────────────────────┘
      ↓
   Indexes: created_at, session_key
   Ordering: -created_at (newest first)
```

## 🚀 Deployment Architecture

```
Development:
  Django runserver → SQLite → Local static files

Production:
  Nginx → Gunicorn → Django App → PostgreSQL
    ↓
  WhiteNoise/CDN for static files
```

## 🎮 Key JavaScript Functions

```javascript
appendValue(value)     // Add digit/operator to expression
deleteLast()          // Remove last character (backspace)
clearAll()            // Reset calculator (AC button)
calculate()           // Submit via HTMX (= button)
updateDisplay()       // Refresh display elements
```

## 📱 Responsive Breakpoints

```
Desktop (> 968px):    Calculator + History side-by-side
Tablet (600-968px):   Calculator + History stacked
Mobile (< 600px):     Smaller buttons, compact layout
Small (< 400px):      Minimum button sizes
```

## 🔧 Technology Stack Summary

| Layer          | Technology          | Purpose                    |
|----------------|---------------------|----------------------------|
| Backend        | Django 5.x          | Web framework              |
| Frontend       | Django Templates    | HTML rendering             |
| Interactivity  | HTMX 1.9+          | Dynamic updates            |
| Styling        | CSS3                | Modern UI design           |
| Database       | SQLite (dev)        | Data persistence           |
| Session        | Django Sessions     | User tracking              |
| Security       | Django Built-in     | CSRF, XSS protection       |

## ⚡ Performance Optimizations

1. **HTMX**: Only HTML fragments transferred (not full JSON)
2. **Local JS**: Immediate display updates before server response
3. **Database Indexing**: Fast history queries by session
4. **Limited History**: Only last 20-50 records loaded
5. **CSS Grid**: Hardware-accelerated layout
6. **Minimal Dependencies**: Faster load times

## 🎯 Next Steps After Setup

1. ✅ Follow IMPLEMENTATION_GUIDE.md
2. ✅ Run migrations
3. ✅ Test basic calculations
4. ✅ Test HTMX interactions
5. ✅ Customize colors/theme
6. ✅ Add more operations (optional)
7. ✅ Deploy to production
