"""
CalorieTracker - Production Flask App
"""
import os
from flask import Flask, render_template
from flask_login import LoginManager

from models import db, User
from seed_data import seed_foods
from models.models import Food


def create_app():
    app = Flask(__name__)

    # --- Config ---
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL', f"sqlite:///{os.path.join(os.path.dirname(__file__), 'calorie_tracker.db')}"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['WTF_CSRF_ENABLED'] = True

    # --- Extensions ---
    db.init_app(app)

    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'warning'

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # --- Blueprints ---
    from blueprints.auth import auth_bp
    from blueprints.dashboard import dashboard_bp
    from blueprints.food import food_bp
    from blueprints.main import main_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(food_bp, url_prefix='/food')
    app.register_blueprint(main_bp)

    # --- Jinja globals ---
    from datetime import timedelta
    app.jinja_env.globals['timedelta'] = timedelta

    # --- Error handlers ---
    @app.errorhandler(404)
    def not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template('errors/500.html'), 500

    # --- DB init + seed ---
    with app.app_context():
        db.create_all()
        seed_foods(db, Food)

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
