"""
Dashboard routes: main view, profile, history, export
"""
import csv
import io
from datetime import date, timedelta
from flask import render_template, redirect, url_for, flash, request, Response, jsonify
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Optional, NumberRange

from models.models import db, DailyLog, LogItem, Food
from . import dashboard_bp


# --- Profile Form ---
class ProfileForm(FlaskForm):
    name = StringField('Full Name', validators=[Optional()])
    age = IntegerField('Age', validators=[Optional(), NumberRange(1, 120)])
    weight = FloatField('Weight (kg)', validators=[Optional(), NumberRange(1, 500)])
    height = FloatField('Height (cm)', validators=[Optional(), NumberRange(50, 300)])
    gender = SelectField('Gender', choices=[('', 'Prefer not to say'), ('male', 'Male'),
                                            ('female', 'Female'), ('other', 'Other')],
                         validators=[Optional()])
    calorie_goal = IntegerField('Daily Calorie Goal', validators=[DataRequired(), NumberRange(500, 10000)])
    protein_goal = FloatField('Protein Goal (g)', validators=[Optional(), NumberRange(0, 500)])
    carbs_goal = FloatField('Carbs Goal (g)', validators=[Optional(), NumberRange(0, 1000)])
    fat_goal = FloatField('Fat Goal (g)', validators=[Optional(), NumberRange(0, 500)])
    submit = SubmitField('Save Profile')


# --- Add Food Log Form ---
class AddLogItemForm(FlaskForm):
    food_id = IntegerField('Food', validators=[DataRequired()])
    grams = FloatField('Amount (g)', validators=[DataRequired(), NumberRange(1, 5000)])
    meal_type = SelectField('Meal', choices=[
        ('breakfast', 'Breakfast'), ('lunch', 'Lunch'),
        ('dinner', 'Dinner'), ('snack', 'Snack')
    ])
    submit = SubmitField('Add to Log')


VALID_MEAL_TYPES = {'breakfast', 'lunch', 'dinner', 'snack'}


def get_or_create_daily_log(user_id, log_date):
    """Get existing DailyLog or create new one"""
    log = DailyLog.query.filter_by(user_id=user_id, log_date=log_date).first()
    if not log:
        log = DailyLog(user_id=user_id, log_date=log_date)
        db.session.add(log)
        db.session.commit()
    return log


@dashboard_bp.route('/')
@login_required
def index():
    log_date_str = request.args.get('date')
    try:
        log_date = date.fromisoformat(log_date_str) if log_date_str else date.today()
    except ValueError:
        log_date = date.today()

    log = DailyLog.query.filter_by(
        user_id=current_user.id, log_date=log_date
    ).first()

    # Group items by meal type
    meals = {'breakfast': [], 'lunch': [], 'dinner': [], 'snack': []}
    if log:
        for item in log.items:
            meals.get(item.meal_type, meals['snack']).append(item)

    # Weekly summary for chart (last 7 days)
    today = date.today()
    weekly_data = []
    for i in range(6, -1, -1):
        d = today - timedelta(days=i)
        wlog = DailyLog.query.filter_by(user_id=current_user.id, log_date=d).first()
        weekly_data.append({
            'date': d.strftime('%a'),
            'calories': wlog.total_calories if wlog else 0,
            'goal': current_user.calorie_goal
        })

    cals_consumed = log.total_calories if log else 0
    cals_goal = current_user.calorie_goal
    pct = min(round(cals_consumed / cals_goal * 100, 1) if cals_goal else 0, 100)
    orb_color = '#00f5c4' if pct < 80 else ('#fbbf24' if pct < 100 else '#f87171')

    form = AddLogItemForm()
    return render_template('dashboard/index.html',
                           log=log,
                           log_date=log_date,
                           today=date.today(),
                           meals=meals,
                           weekly_data=weekly_data,
                           cals_consumed=cals_consumed,
                           cals_goal=cals_goal,
                           cals_remaining=cals_goal - cals_consumed,
                           pct=pct,
                           orb_color=orb_color,
                           form=form)


@dashboard_bp.route('/add-item', methods=['POST'])
@login_required
def add_item():
    food_id = request.form.get('food_id', type=int)
    grams = request.form.get('grams', type=float)
    meal_type = request.form.get('meal_type', 'snack')
    log_date_str = request.form.get('log_date', date.today().isoformat())

    try:
        log_date = date.fromisoformat(log_date_str)
    except ValueError:
        log_date = date.today()

    if food_id is None:
        flash('Food is required.', 'danger')
        return redirect(url_for('dashboard.index', date=log_date_str))

    if grams is None or grams <= 0:
        flash('Amount must be greater than 0 grams.', 'danger')
        return redirect(url_for('dashboard.index', date=log_date_str))

    if meal_type not in VALID_MEAL_TYPES:
        flash('Invalid meal type.', 'danger')
        return redirect(url_for('dashboard.index', date=log_date_str))

    food = Food.query.filter(
        Food.id == food_id,
        (Food.is_system == True) | (Food.user_id == current_user.id)
    ).first()
    if not food:
        flash('Food not found or not available to your account.', 'danger')
        return redirect(url_for('dashboard.index', date=log_date_str))

    log = get_or_create_daily_log(current_user.id, log_date)

    item = LogItem(daily_log_id=log.id, food_id=food.id,
                   grams=grams, meal_type=meal_type, food=food)
    item.calculate_from_food()
    db.session.add(item)
    log.recalculate_totals()
    db.session.commit()

    flash(f'Added {food.name} ({grams}g) to {meal_type}.', 'success')
    return redirect(url_for('dashboard.index', date=log_date_str))


@dashboard_bp.route('/remove-item/<int:item_id>', methods=['POST'])
@login_required
def remove_item(item_id):
    item = LogItem.query.get_or_404(item_id)
    log = item.daily_log
    if log.user_id != current_user.id:
        flash('Unauthorized.', 'danger')
        return redirect(url_for('dashboard.index'))
    log_date_str = log.log_date.isoformat()
    db.session.delete(item)
    log.recalculate_totals()
    db.session.commit()
    flash('Item removed.', 'info')
    return redirect(url_for('dashboard.index', date=log_date_str))


@dashboard_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.age = form.age.data
        current_user.weight = form.weight.data
        current_user.height = form.height.data
        current_user.gender = form.gender.data
        current_user.calorie_goal = form.calorie_goal.data
        current_user.protein_goal = form.protein_goal.data or 0
        current_user.carbs_goal = form.carbs_goal.data or 0
        current_user.fat_goal = form.fat_goal.data or 0
        db.session.commit()
        flash('Profile updated!', 'success')
        return redirect(url_for('dashboard.profile'))
    return render_template('dashboard/profile.html', form=form)


@dashboard_bp.route('/history')
@login_required
def history():
    page = request.args.get('page', 1, type=int)
    period = request.args.get('period', 'week')  # week/month

    logs = DailyLog.query.filter_by(user_id=current_user.id)\
        .order_by(DailyLog.log_date.desc())\
        .paginate(page=page, per_page=14, error_out=False)

    return render_template('dashboard/history.html', logs=logs, period=period)


@dashboard_bp.route('/export/csv')
@login_required
def export_csv():
    logs = DailyLog.query.filter_by(user_id=current_user.id)\
        .order_by(DailyLog.log_date.desc()).all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Date', 'Calories', 'Protein (g)', 'Carbs (g)', 'Fat (g)', 'Fiber (g)'])
    for log in logs:
        writer.writerow([
            log.log_date, round(log.total_calories, 1),
            round(log.total_protein, 1), round(log.total_carbs, 1),
            round(log.total_fat, 1), round(log.total_fiber, 1)
        ])
    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=calorie_log.csv'}
    )


@dashboard_bp.route('/export/pdf')
@login_required
def export_pdf():
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib import colors

        logs = DailyLog.query.filter_by(user_id=current_user.id)\
            .order_by(DailyLog.log_date.desc()).limit(30).all()

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []

        elements.append(Paragraph(f'Calorie Report - {current_user.username}', styles['Title']))
        elements.append(Spacer(1, 12))

        data = [['Date', 'Calories', 'Protein', 'Carbs', 'Fat']]
        for log in logs:
            data.append([
                str(log.log_date),
                f'{log.total_calories:.0f}',
                f'{log.total_protein:.1f}g',
                f'{log.total_carbs:.1f}g',
                f'{log.total_fat:.1f}g'
            ])

        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0f172a')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f1f5f9')]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        elements.append(table)
        doc.build(elements)
        buffer.seek(0)

        return Response(
            buffer.getvalue(),
            mimetype='application/pdf',
            headers={'Content-Disposition': 'attachment; filename=calorie_report.pdf'}
        )
    except ImportError:
        flash('PDF export requires reportlab. Run: pip install reportlab', 'warning')
        return redirect(url_for('dashboard.history'))


@dashboard_bp.route('/api/weekly-data')
@login_required
def api_weekly_data():
    """JSON endpoint for chart data"""
    today = date.today()
    data = []
    for i in range(6, -1, -1):
        d = today - timedelta(days=i)
        log = DailyLog.query.filter_by(user_id=current_user.id, log_date=d).first()
        data.append({
            'date': d.strftime('%a'),
            'calories': round(log.total_calories if log else 0),
            'protein': round(log.total_protein if log else 0, 1),
            'carbs': round(log.total_carbs if log else 0, 1),
            'fat': round(log.total_fat if log else 0, 1),
        })
    return jsonify(data)
