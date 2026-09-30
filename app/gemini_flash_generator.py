import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY", "")
MODEL_NAME = os.getenv("GEMINI_FLASH_MODEL", "gemini-1.5-flash")

genai_configured = False
if API_KEY and API_KEY != "your_gemini_api_key_here":
    try:
        import google.generativeai as genai
        genai.configure(api_key=API_KEY)
        genai_configured = True
    except Exception as e:
        print(f"Warning: Could not configure Gemini Flash: {e}")


def _fallback_tip(goal: str) -> str:
    goal_lower = goal.lower()
    if "muscle" in goal_lower or "bulk" in goal_lower or "strength" in goal_lower:
        return "Prioritize protein! Aim for 1.6 to 2.2 grams of protein per kilogram of body weight spread evenly across 3-4 meals (sources like chicken breast, fish, eggs, tofu, and Greek yogurt). Also consume a balanced carbohydrate-and-protein snack within 45 minutes post-workout to fuel muscle protein synthesis."
    elif "loss" in goal_lower or "fat" in goal_lower or "cut" in goal_lower:
        return "Prioritize high-volume, nutrient-dense foods! Fill half of your plate with fibrous green vegetables, maintain a moderate caloric deficit (300-500 kcal below maintenance), and drink 500ml of cold water 20 minutes before meals to promote fullness and optimal metabolic rate."
    elif "flexibility" in goal_lower or "mobility" in goal_lower or "recovery" in goal_lower:
        return "Stay hydrated and replenish electrolytes! Ensure your diet includes rich magnesium sources like almonds, spinach, and avocados to relax neuromuscular tension, and hydrate with water and a pinch of pink salt to lubricate connective tissues."
    else:
        return "Focus on the 80/20 rule: make 80% of your meals whole, unprocessed foods rich in micronutrients and fiber, while allowing 20% flexibility. Pair daily hydration (at least 2.5-3 liters) with 7-8 hours of sound sleep to maximize physical vitality!"


def generate_nutrition_tip_with_flash(goal: str) -> str:
    """
    Generate a nutrition or recovery tip using Gemini Flash based on the user's fitness goal.

    Args:
        goal (str): User's fitness goal - "weight loss", "muscle gain", or "general fitness".

    Returns:
        str: Generated tip.
    """
    prompt = (
        f"Give one clear, helpful nutrition or recovery tip for someone focused on '{goal}'. "
        "The tip should be practical, friendly, and easy to understand. Keep it to 2-3 engaging sentences."
    )

    if genai_configured:
        try:
            import google.generativeai as genai
            model = genai.GenerativeModel(MODEL_NAME)
            response = model.generate_content(prompt)
            if response and response.text:
                return response.text.strip()
        except Exception as e:
            print(f"Gemini Flash tip generation error: {e}. Using goal-aligned fallback tip.")
            return _fallback_tip(goal)

    return _fallback_tip(goal)
