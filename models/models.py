"""
Database models for CalorieTracker
"""
from datetime import date
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """User account + profile data"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    # Profile
    name = db.Column(db.String(120))
    age = db.Column(db.Integer)
    weight = db.Column(db.Float)   # kg
    height = db.Column(db.Float)   # cm
    gender = db.Column(db.String(10))

    # Goals
    calorie_goal = db.Column(db.Integer, default=2000)
    protein_goal = db.Column(db.Float, default=150.0)  # grams
    carbs_goal = db.Column(db.Float, default=250.0)
    fat_goal = db.Column(db.Float, default=65.0)

    # Relationships
    daily_logs = db.relationship('DailyLog', back_populates='user', cascade='all, delete-orphan')
    custom_foods = db.relationship('Food', back_populates='creator', cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


class Food(db.Model):
    """Food item (preloaded + custom). Values per 100g."""
    __tablename__ = 'foods'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    brand = db.Column(db.String(100))
    category = db.Column(db.String(50))

    # Per 100g macros
    calories = db.Column(db.Float, nullable=False)
    protein = db.Column(db.Float, default=0.0)
    carbs = db.Column(db.Float, default=0.0)
    fat = db.Column(db.Float, default=0.0)
    fiber = db.Column(db.Float, default=0.0)
    sugar = db.Column(db.Float, default=0.0)

    # Is preloaded system food or user-created
    is_system = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    creator = db.relationship('User', back_populates='custom_foods')
    log_items = db.relationship('LogItem', back_populates='food')

    def macros_for_grams(self, grams):
        """Return dict of macros scaled to given gram quantity"""
        ratio = grams / 100.0
        return {
            'calories': round(self.calories * ratio, 1),
            'protein': round(self.protein * ratio, 1),
            'carbs': round(self.carbs * ratio, 1),
            'fat': round(self.fat * ratio, 1),
            'fiber': round(self.fiber * ratio, 1),
        }

    def __repr__(self):
        return f'<Food {self.name}>'


class DailyLog(db.Model):
    """One log per user per day"""
    __tablename__ = 'daily_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    log_date = db.Column(db.Date, nullable=False, default=date.today)

    # Cached totals (recalculated on each update)
    total_calories = db.Column(db.Float, default=0.0)
    total_protein = db.Column(db.Float, default=0.0)
    total_carbs = db.Column(db.Float, default=0.0)
    total_fat = db.Column(db.Float, default=0.0)
    total_fiber = db.Column(db.Float, default=0.0)

    notes = db.Column(db.Text)

    user = db.relationship('User', back_populates='daily_logs')
    items = db.relationship('LogItem', back_populates='daily_log', cascade='all, delete-orphan')

    __table_args__ = (db.UniqueConstraint('user_id', 'log_date', name='uq_user_date'),)

    def recalculate_totals(self):
        """Recompute cached totals from items"""
        self.total_calories = sum(i.calories for i in self.items)
        self.total_protein = sum(i.protein for i in self.items)
        self.total_carbs = sum(i.carbs for i in self.items)
        self.total_fat = sum(i.fat for i in self.items)
        self.total_fiber = sum(i.fiber for i in self.items)

    def __repr__(self):
        return f'<DailyLog {self.log_date} user={self.user_id}>'


class LogItem(db.Model):
    """Single food entry within a daily log"""
    __tablename__ = 'log_items'

    id = db.Column(db.Integer, primary_key=True)
    daily_log_id = db.Column(db.Integer, db.ForeignKey('daily_logs.id'), nullable=False)
    food_id = db.Column(db.Integer, db.ForeignKey('foods.id'), nullable=False)
    grams = db.Column(db.Float, nullable=False)
    meal_type = db.Column(db.String(20), default='snack')  # breakfast/lunch/dinner/snack

    # Stored calculated values (snapshot, food may change)
    calories = db.Column(db.Float, default=0.0)
    protein = db.Column(db.Float, default=0.0)
    carbs = db.Column(db.Float, default=0.0)
    fat = db.Column(db.Float, default=0.0)
    fiber = db.Column(db.Float, default=0.0)

    daily_log = db.relationship('DailyLog', back_populates='items')
    food = db.relationship('Food', back_populates='log_items')

    def calculate_from_food(self):
        """Compute and store macros from food + grams"""
        macros = self.food.macros_for_grams(self.grams)
        self.calories = macros['calories']
        self.protein = macros['protein']
        self.carbs = macros['carbs']
        self.fat = macros['fat']
        self.fiber = macros['fiber']

    def __repr__(self):
        return f'<LogItem food={self.food_id} grams={self.grams}>'
