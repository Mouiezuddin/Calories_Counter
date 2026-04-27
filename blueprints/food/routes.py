"""
Food management: list, search, add custom, delete
"""
from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional

from models.models import db, Food
from . import food_bp


class FoodForm(FlaskForm):
    name = StringField('Food Name', validators=[DataRequired()])
    brand = StringField('Brand', validators=[Optional()])
    category = SelectField('Category', choices=[
        ('', 'Select category'),
        ('Protein', 'Protein'), ('Grains', 'Grains'),
        ('Vegetables', 'Vegetables'), ('Fruit', 'Fruit'),
        ('Dairy', 'Dairy'), ('Fats', 'Fats'), ('Nuts', 'Nuts'),
        ('Snacks', 'Snacks'), ('Supplement', 'Supplement'), ('Other', 'Other'),
    ], validators=[Optional()])
    calories = FloatField('Calories (per 100g)', validators=[DataRequired(), NumberRange(0, 9000)])
    protein = FloatField('Protein (g)', validators=[Optional(), NumberRange(0, 100)])
    carbs = FloatField('Carbs (g)', validators=[Optional(), NumberRange(0, 100)])
    fat = FloatField('Fat (g)', validators=[Optional(), NumberRange(0, 100)])
    fiber = FloatField('Fiber (g)', validators=[Optional(), NumberRange(0, 100)])
    submit = SubmitField('Save Food')


@food_bp.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    q = request.args.get('q', '').strip()
    category = request.args.get('category', '')

    query = Food.query.filter(
        (Food.is_system == True) | (Food.user_id == current_user.id)
    )
    if q:
        query = query.filter(Food.name.ilike(f'%{q}%'))
    if category:
        query = query.filter(Food.category == category)

    foods = query.order_by(Food.is_system.desc(), Food.name).paginate(
        page=page, per_page=20, error_out=False
    )

    categories = db.session.query(Food.category).filter(
        Food.category.isnot(None)
    ).distinct().all()
    categories = sorted([c[0] for c in categories if c[0]])

    form = FoodForm()
    return render_template('food/index.html', foods=foods, form=form,
                           q=q, category=category, categories=categories)


@food_bp.route('/add', methods=['POST'])
@login_required
def add():
    form = FoodForm()
    if form.validate_on_submit():
        food = Food(
            name=form.name.data,
            brand=form.brand.data,
            category=form.category.data or 'Other',
            calories=form.calories.data,
            protein=form.protein.data or 0,
            carbs=form.carbs.data or 0,
            fat=form.fat.data or 0,
            fiber=form.fiber.data or 0,
            is_system=False,
            user_id=current_user.id
        )
        db.session.add(food)
        db.session.commit()
        flash(f'"{food.name}" added to your foods!', 'success')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{field}: {error}', 'danger')
    return redirect(url_for('food.index'))


@food_bp.route('/delete/<int:food_id>', methods=['POST'])
@login_required
def delete(food_id):
    food = Food.query.get_or_404(food_id)
    if food.user_id != current_user.id:
        flash('Cannot delete system or other users\' foods.', 'danger')
        return redirect(url_for('food.index'))
    db.session.delete(food)
    db.session.commit()
    flash(f'"{food.name}" deleted.', 'info')
    return redirect(url_for('food.index'))


@food_bp.route('/search')
@login_required
def search():
    """JSON endpoint for food search autocomplete"""
    q = request.args.get('q', '').strip()
    if len(q) < 2:
        return jsonify([])
    foods = Food.query.filter(
        Food.name.ilike(f'%{q}%'),
        (Food.is_system == True) | (Food.user_id == current_user.id)
    ).order_by(Food.is_system.desc()).limit(10).all()
    return jsonify([{
        'id': f.id,
        'name': f.name,
        'category': f.category,
        'calories': f.calories,
        'protein': f.protein,
        'carbs': f.carbs,
        'fat': f.fat,
    } for f in foods])
