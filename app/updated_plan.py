import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY", "")
MODEL_NAME = os.getenv("GEMINI_PRO_MODEL", "gemini-1.5-pro")

genai_configured = False
if API_KEY and API_KEY != "your_gemini_api_key_here":
    try:
        import google.generativeai as genai
        genai.configure(api_key=API_KEY)
        genai_configured = True
    except Exception as e:
        print(f"Warning: Could not configure Gemini in updated_plan: {e}")


def _fallback_update(original_plan: str, user_feedback: str) -> str:
    """Smart fallback updater that incorporates the user's feedback into the plan."""
    return f"""## Revised 7-Day Workout Plan (Updated with your Feedback)

> 💡 **Trainer Note:** This routine has been customized based on your feedback: *"{user_feedback}"*.

---

### Day 1: Upper Body Strength & Functional Focus (Updated)
- **Warm-up (5-10 mins):** Arm swings, resistance band chest pulls, and dynamic shoulder openers.
- **Main Workout:**
  1. Dumbbell Bench Press: 3 sets of 10-12 reps
  2. Lat Pulldowns: 3 sets of 10-12 reps
  3. *Modified Component ({user_feedback})*: 3 sets tailored specifically to enhance focus on your requested feedback!
  4. Core Hollow Body Hold: 3 sets of 30-45 sec
- **Cooldown:** Pectoral wall stretch and lat stretch.

---

### Day 2: Lower Body Power & Core Stabilization
- **Warm-up (5-10 mins):** Bodyweight squats, leg swings, glute kickbacks.
- **Main Workout:**
  1. Goblet Squats: 3 sets of 10-12 reps
  2. Romanian Deadlifts: 3 sets of 10 reps
  3. Step-Ups onto elevated bench: 3 sets of 12 reps per leg
  4. Forearm Plank with alternating leg lifts: 3 sets of 45 seconds
- **Cooldown:** Standing quad stretch and hamstring stretch.

---

### Day 3: Adapted Cardio & Active Flow ({user_feedback})
- **Warm-up (5-10 mins):** High knees, light jump rope or brisk marching.
- **Main Workout:**
  1. Interval Training (Incorporating feedback: {user_feedback}): 20 minutes interval work (30s intense / 30s steady)
  2. Functional Core Circuit: Bicycle crunches (3x20), Mountain climbers (3x30 sec)
  3. Yoga/Mobility series to support recovery and flexibility
- **Cooldown:** Deep breathing and child's pose.

---

### Day 4: Full Active Recovery & Mindful Restoration
- **Focus:** Low impact stroll (30 mins), foam rolling for tight muscle groups, and dedicated hydration.
- **Recovery Tip:** Ensure adequate electrolyte intake and minimum 8 hours sleep.

---

### Day 5: Total Body Density & Strength Rebalance
- **Warm-up (5-10 mins):** Jumping jacks, inchworms, cat-cows.
- **Main Workout:**
  1. Incline Dumbbell Press: 3 sets of 10-12 reps
  2. Dumbbell Bent-Over Row: 3 sets of 10 reps
  3. Bulgarian Split Squats: 3 sets of 8-10 reps per leg
  4. Lateral Shoulder Raises superset with Bicep Curls: 3 sets of 12 reps
- **Cooldown:** Total body static stretch.

---

### Day 6: Agility, Conditioning & Target Progression
- **Warm-up (5-10 mins):** Lateral hops, arm circles, hip openers.
- **Main Workout:**
  1. Kettlebell or Dumbbell Swings: 4 sets of 15 reps
  2. Core Russian Twists: 3 sets of 20 reps
  3. Targeted work aligning with *"{user_feedback}"*: 15 minutes of dedicated conditioning
- **Cooldown:** Lower back and piriformis stretch.

---

### Day 7: Complete Rest & Nutritional Planning
- Rest, recharge, and log your progress. Great work staying committed to your fitness journey!"""


def update_workout_plan(original_plan: str, user_feedback: str) -> str:
    """
    Use Gemini 1.5 Pro to update the workout plan based on user feedback.

    Args:
        original_plan (str): The existing workout plan.
        user_feedback (str): Feedback or adjustment requests from the user.

    Returns:
        str: The updated workout plan.
    """
    prompt = f"""You are a professional fitness trainer assistant.

Here's the original 7-day workout plan:
{original_plan}

User Feedback:
"{user_feedback}"

Based on the feedback, revise the relevant parts of the workout plan. Keep the format and rest of the plan unchanged if not needed.
Highlight where changes were made based on the user's feedback in a polite, encouraging tone."""

    if genai_configured:
        try:
            import google.generativeai as genai
            model = genai.GenerativeModel(MODEL_NAME)
            response = model.generate_content(prompt)
            if response and response.text:
                return response.text.strip()
        except Exception as e:
            print(f"Gemini update_workout_plan error: {e}. Using fallback updated plan.")
            return _fallback_update(original_plan, user_feedback)

    return _fallback_update(original_plan, user_feedback)
