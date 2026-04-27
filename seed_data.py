"""Preload common foods into DB"""
SEED_FOODS = [
    # Proteins
    {"name": "Chicken Breast (cooked)", "category": "Protein", "calories": 165, "protein": 31, "carbs": 0, "fat": 3.6, "fiber": 0},
    {"name": "Eggs (whole)", "category": "Protein", "calories": 155, "protein": 13, "carbs": 1.1, "fat": 11, "fiber": 0},
    {"name": "Tuna (canned in water)", "category": "Protein", "calories": 116, "protein": 25.5, "carbs": 0, "fat": 1, "fiber": 0},
    {"name": "Salmon (cooked)", "category": "Protein", "calories": 208, "protein": 20, "carbs": 0, "fat": 13, "fiber": 0},
    {"name": "Greek Yogurt (plain)", "category": "Dairy", "calories": 59, "protein": 10, "carbs": 3.6, "fat": 0.4, "fiber": 0},
    {"name": "Cottage Cheese", "category": "Dairy", "calories": 98, "protein": 11, "carbs": 3.4, "fat": 4.3, "fiber": 0},
    {"name": "Whey Protein Powder", "category": "Supplement", "calories": 373, "protein": 80, "carbs": 6, "fat": 5, "fiber": 0},
    {"name": "Beef (lean ground)", "category": "Protein", "calories": 218, "protein": 26, "carbs": 0, "fat": 12, "fiber": 0},
    {"name": "Turkey Breast", "category": "Protein", "calories": 135, "protein": 30, "carbs": 0, "fat": 1, "fiber": 0},
    {"name": "Tofu (firm)", "category": "Protein", "calories": 76, "protein": 8, "carbs": 1.9, "fat": 4.8, "fiber": 0.3},

    # Carbs/Grains
    {"name": "White Rice (cooked)", "category": "Grains", "calories": 130, "protein": 2.7, "carbs": 28, "fat": 0.3, "fiber": 0.4},
    {"name": "Brown Rice (cooked)", "category": "Grains", "calories": 112, "protein": 2.6, "carbs": 24, "fat": 0.9, "fiber": 1.8},
    {"name": "Oats (dry)", "category": "Grains", "calories": 389, "protein": 17, "carbs": 66, "fat": 7, "fiber": 11},
    {"name": "Whole Wheat Bread", "category": "Grains", "calories": 247, "protein": 13, "carbs": 41, "fat": 4, "fiber": 7},
    {"name": "White Bread", "category": "Grains", "calories": 265, "protein": 9, "carbs": 49, "fat": 3.2, "fiber": 2.3},
    {"name": "Pasta (cooked)", "category": "Grains", "calories": 131, "protein": 5, "carbs": 25, "fat": 1.1, "fiber": 1.8},
    {"name": "Quinoa (cooked)", "category": "Grains", "calories": 120, "protein": 4.4, "carbs": 22, "fat": 1.9, "fiber": 2.8},
    {"name": "Potato (baked)", "category": "Vegetables", "calories": 93, "protein": 2.5, "carbs": 21, "fat": 0.1, "fiber": 2.2},
    {"name": "Sweet Potato (baked)", "category": "Vegetables", "calories": 86, "protein": 1.6, "carbs": 20, "fat": 0.1, "fiber": 3},

    # Vegetables
    {"name": "Broccoli", "category": "Vegetables", "calories": 34, "protein": 2.8, "carbs": 7, "fat": 0.4, "fiber": 2.6},
    {"name": "Spinach", "category": "Vegetables", "calories": 23, "protein": 2.9, "carbs": 3.6, "fat": 0.4, "fiber": 2.2},
    {"name": "Kale", "category": "Vegetables", "calories": 49, "protein": 4.3, "carbs": 9, "fat": 0.9, "fiber": 3.6},
    {"name": "Bell Pepper", "category": "Vegetables", "calories": 31, "protein": 1, "carbs": 6, "fat": 0.3, "fiber": 2.1},
    {"name": "Carrot", "category": "Vegetables", "calories": 41, "protein": 0.9, "carbs": 10, "fat": 0.2, "fiber": 2.8},
    {"name": "Cucumber", "category": "Vegetables", "calories": 16, "protein": 0.7, "carbs": 4, "fat": 0.1, "fiber": 0.5},
    {"name": "Tomato", "category": "Vegetables", "calories": 18, "protein": 0.9, "carbs": 3.9, "fat": 0.2, "fiber": 1.2},
    {"name": "Avocado", "category": "Fruit", "calories": 160, "protein": 2, "carbs": 9, "fat": 15, "fiber": 7},

    # Fruits
    {"name": "Banana", "category": "Fruit", "calories": 89, "protein": 1.1, "carbs": 23, "fat": 0.3, "fiber": 2.6},
    {"name": "Apple", "category": "Fruit", "calories": 52, "protein": 0.3, "carbs": 14, "fat": 0.2, "fiber": 2.4},
    {"name": "Orange", "category": "Fruit", "calories": 47, "protein": 0.9, "carbs": 12, "fat": 0.1, "fiber": 2.4},
    {"name": "Blueberries", "category": "Fruit", "calories": 57, "protein": 0.7, "carbs": 14, "fat": 0.3, "fiber": 2.4},
    {"name": "Strawberries", "category": "Fruit", "calories": 32, "protein": 0.7, "carbs": 7.7, "fat": 0.3, "fiber": 2},

    # Fats
    {"name": "Olive Oil", "category": "Fats", "calories": 884, "protein": 0, "carbs": 0, "fat": 100, "fiber": 0},
    {"name": "Butter", "category": "Fats", "calories": 717, "protein": 0.9, "carbs": 0.1, "fat": 81, "fiber": 0},
    {"name": "Peanut Butter", "category": "Fats", "calories": 588, "protein": 25, "carbs": 20, "fat": 50, "fiber": 6},
    {"name": "Almonds", "category": "Nuts", "calories": 579, "protein": 21, "carbs": 22, "fat": 50, "fiber": 13},
    {"name": "Walnuts", "category": "Nuts", "calories": 654, "protein": 15, "carbs": 14, "fat": 65, "fiber": 6.7},

    # Dairy
    {"name": "Whole Milk", "category": "Dairy", "calories": 61, "protein": 3.2, "carbs": 4.8, "fat": 3.3, "fiber": 0},
    {"name": "Cheddar Cheese", "category": "Dairy", "calories": 403, "protein": 25, "carbs": 1.3, "fat": 33, "fiber": 0},
    {"name": "Mozzarella", "category": "Dairy", "calories": 280, "protein": 22, "carbs": 2.2, "fat": 22, "fiber": 0},

    # Snacks/Other
    {"name": "Dark Chocolate (70%)", "category": "Snacks", "calories": 598, "protein": 7.8, "carbs": 46, "fat": 43, "fiber": 11},
    {"name": "Rice Cakes", "category": "Snacks", "calories": 387, "protein": 8, "carbs": 82, "fat": 2.8, "fiber": 1.3},
    {"name": "Protein Bar (avg)", "category": "Snacks", "calories": 350, "protein": 20, "carbs": 40, "fat": 10, "fiber": 5},
]


def seed_foods(db, Food):
    """Insert system foods if not already present"""
    if Food.query.filter_by(is_system=True).count() > 0:
        return
    for food_data in SEED_FOODS:
        food = Food(
            name=food_data["name"],
            category=food_data.get("category"),
            calories=food_data["calories"],
            protein=food_data.get("protein", 0),
            carbs=food_data.get("carbs", 0),
            fat=food_data.get("fat", 0),
            fiber=food_data.get("fiber", 0),
            is_system=True,
            user_id=None
        )
        db.session.add(food)
    db.session.commit()
    print(f"Seeded {len(SEED_FOODS)} system foods.")
