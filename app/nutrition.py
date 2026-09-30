"""
FitBuddy Nutrition Helper Module
Provides baseline nutrition calculations (BMR, TDEE, macro breakdowns)
and goal-specific dietary guidance to complement Gemini Flash generated tips.
"""

def calculate_bmr(weight_kg: float, age: int, gender: str = "neutral") -> float:
    """Estimates Basal Metabolic Rate using Mifflin-St Jeor formula."""
    base = 10 * weight_kg + 6.25 * 170 - 5 * age
    return base


def get_macronutrient_recommendations(goal: str, weight_kg: float) -> dict:
    """
    Returns daily macronutrient guidance targets based on fitness goal and weight.
    """
    goal_lower = goal.lower()
    if "muscle" in goal_lower or "bulk" in goal_lower:
        protein_g = round(weight_kg * 2.0, 1)
        fats_g = round(weight_kg * 0.9, 1)
        carbs_g = round(weight_kg * 3.5, 1)
        calorie_multiplier = 33
    elif "loss" in goal_lower or "cut" in goal_lower or "fat" in goal_lower:
        protein_g = round(weight_kg * 2.2, 1)
        fats_g = round(weight_kg * 0.7, 1)
        carbs_g = round(weight_kg * 2.0, 1)
        calorie_multiplier = 25
    else:
        protein_g = round(weight_kg * 1.6, 1)
        fats_g = round(weight_kg * 0.8, 1)
        carbs_g = round(weight_kg * 2.8, 1)
        calorie_multiplier = 29

    estimated_calories = round(weight_kg * calorie_multiplier)

    return {
        "calories": estimated_calories,
        "protein_grams": protein_g,
        "fats_grams": fats_g,
        "carbs_grams": carbs_g,
        "water_liters": round(weight_kg * 0.035, 1)
    }
