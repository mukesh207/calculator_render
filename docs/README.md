# Django HTMX Calculator

A modern, responsive calculator web application built with Django and HTMX.

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation & Setup

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd calculator_project
```

2. **Create and activate virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run database migrations**
```bash
python manage.py migrate
```

5. **Start the development server**
```bash
python manage.py runserver
```

6. **Open your browser**
Visit: http://127.0.0.1:8000/

## Features
- ✨ Real-time calculations without page reload (HTMX)
- 🎨 Modern, responsive UI design
- 📊 Calculation history tracking
- ⌨️ Keyboard support
- 📱 Mobile-friendly interface
- 🔒 Secure calculation processing

## Technology Stack
- Django 5.x
- HTMX for dynamic interactions
- SQLite database
- Vanilla CSS3 for styling

## Project Structure
See `PROJECT_PLAN.md` for detailed architecture and implementation guide.

## Development Notes
- All HTMX endpoints return HTML fragments
- Calculations are saved to database automatically
- History is session-specific
- No JavaScript framework required (HTMX handles it)

## License
MIT License
