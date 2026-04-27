import os
import tempfile
import unittest
from pathlib import Path


class CalorieTrackerTestCase(unittest.TestCase):
    def setUp(self):
        fd, db_path = tempfile.mkstemp(suffix=".db")
        os.close(fd)
        self.db_path = db_path
        os.environ["DATABASE_URL"] = f"sqlite:///{Path(db_path).as_posix()}"
        os.environ["SECRET_KEY"] = "test-secret"

        from app import create_app
        from models.models import db

        self.app = create_app()
        self.app.config.update(TESTING=True, WTF_CSRF_ENABLED=False)
        self.client = self.app.test_client()
        self.db = db

    def tearDown(self):
        with self.app.app_context():
            self.db.session.remove()
            self.db.drop_all()
            self.db.engine.dispose()
        os.environ.pop("DATABASE_URL", None)
        os.environ.pop("SECRET_KEY", None)

    def register_and_login(self, username="tester", email="tester@example.com"):
        response = self.client.post(
            "/auth/register",
            data={
                "username": username,
                "email": email,
                "password": "password123",
                "confirm_password": "password123",
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            "/auth/login",
            data={"email": email, "password": "password123"},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)

    def test_dashboard_happy_path(self):
        from models.models import DailyLog, Food, LogItem

        self.register_and_login()

        with self.app.app_context():
            food = Food.query.filter_by(is_system=True).first()
            self.assertIsNotNone(food)

        response = self.client.post(
            "/dashboard/add-item",
            data={"food_id": food.id, "grams": "150", "meal_type": "breakfast"},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Added", response.data)

        with self.app.app_context():
            log = DailyLog.query.first()
            item = LogItem.query.first()
            self.assertIsNotNone(log)
            self.assertIsNotNone(item)
            self.assertGreater(log.total_calories, 0)

    def test_add_item_rejects_invalid_grams(self):
        from models.models import DailyLog, Food, LogItem

        self.register_and_login()

        with self.app.app_context():
            food = Food.query.filter_by(is_system=True).first()

        response = self.client.post(
            "/dashboard/add-item",
            data={"food_id": food.id, "grams": "", "meal_type": "breakfast"},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Amount must be greater than 0 grams.", response.data)

        with self.app.app_context():
            self.assertEqual(DailyLog.query.count(), 0)
            self.assertEqual(LogItem.query.count(), 0)

    def test_add_item_rejects_other_users_custom_food(self):
        from models.models import Food, User, db

        self.register_and_login(username="owneruser", email="owner@example.com")

        with self.app.app_context():
            owner = User.query.filter_by(email="owner@example.com").first()
            private_food = Food(
                name="Owner Secret Food",
                brand="Private",
                category="Other",
                calories=321,
                is_system=False,
                user_id=owner.id,
            )
            db.session.add(private_food)
            db.session.commit()
            private_food_id = private_food.id

        self.client.get("/auth/logout", follow_redirects=True)
        self.register_and_login(username="otheruser", email="other@example.com")

        response = self.client.post(
            "/dashboard/add-item",
            data={"food_id": private_food_id, "grams": "100", "meal_type": "lunch"},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Food not found or not available to your account.", response.data)

    def test_dashboard_tolerates_invalid_saved_meal_type(self):
        from datetime import date
        from models.models import DailyLog, Food, LogItem, User, db

        self.register_and_login()

        with self.app.app_context():
            user = User.query.filter_by(email="tester@example.com").first()
            food = Food.query.filter_by(is_system=True).first()
            log = DailyLog(user_id=user.id, log_date=date.today())
            db.session.add(log)
            db.session.flush()
            item = LogItem(
                daily_log_id=log.id,
                food_id=food.id,
                grams=100,
                meal_type="brunch",
                food=food,
            )
            item.calculate_from_food()
            db.session.add(item)
            log.recalculate_totals()
            db.session.commit()

        response = self.client.get("/dashboard/")
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
