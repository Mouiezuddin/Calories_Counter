# NutriCore — Calorie Tracker

Production-ready Flask calorie tracker with 3D Three.js UI, Anime.js animations, Chart.js analytics.

## Tech Stack
- **Backend**: Flask, SQLAlchemy, Flask-Login, Flask-WTF
- **DB**: SQLite (auto-created)
- **Frontend**: Tailwind CSS, Three.js, Anime.js, Chart.js

## Setup

```bash
# 1. Clone / unzip project
cd calorie_tracker

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run
python app.py
```

Visit http://localhost:5000

## Features
- **Auth**: Register, login, logout with secure password hashing
- **Profile**: Name, age, weight, height, BMI calculator, macro goals
- **Dashboard**: 3D calorie orb (green→yellow→red), macro bars, Charts
- **Food DB**: 43 preloaded foods + custom food creation
- **Daily Log**: Add foods by grams, grouped by meal type (breakfast/lunch/dinner/snack)
- **History**: Paginated log table with color-coded calorie diff vs goal
- **Export**: CSV download, PDF report (requires reportlab)
- **3D**: Three.js particle background + rotating calorie orb
- **Animations**: Anime.js page transitions, counters, particle burst on food add

## Project Structure
```
calorie_tracker/
├── app.py                    # App factory
├── models/
│   └── models.py             # User, Food, DailyLog, LogItem
├── blueprints/
│   ├── auth/                 # Register, login, logout
│   ├── dashboard/            # Main dashboard, profile, history, export
│   ├── food/                 # Food CRUD + search API
│   └── main/                 # Landing page
├── templates/
│   ├── base.html             # Base with Three.js bg + Anime.js
│   ├── auth/
│   ├── dashboard/
│   ├── food/
│   ├── main/
│   └── errors/              # 404, 500 pages
├── seed_data.py              # 43 preloaded foods
└── requirements.txt
```

## Environment Variables (optional)
Copy `.env.example` to `.env` and configure:
```
SECRET_KEY=your-secure-random-key-here
DATABASE_URL=sqlite:///calorie_tracker.db
FLASK_ENV=development
FLASK_DEBUG=False
```

**Note**: Never commit `.env` files with real secrets. Use `.env.example` as a template.

## Default Ports
App runs on http://localhost:5000
