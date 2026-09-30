import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY", "")
MODEL_NAME = os.getenv("GEMINI_PRO_MODEL", "gemini-1.5-pro")

# Configure Google Generative AI if key is provided and not default placeholder
genai_configured = False
if API_KEY and API_KEY != "your_gemini_api_key_here":
    try:
        import google.generativeai as genai
        genai.configure(api_key=API_KEY)
        genai_configured = True
    except Exception as e:
        print(f"Warning: Could not configure Google Generative AI: {e}")


def _generate_fallback_plan(goal: str, intensity: str) -> str:
    """Provides a realistic, structured 7-day workout plan if API key is not configured or fails."""
    return f"""## 7-Day {intensity.capitalize()} Intensity Workout Plan for {goal.title()}

This plan balances progressive resistance, cardiovascular conditioning, and dedicated recovery tailored to your fitness level. Hydrate consistently and execute each movement with proper biomechanics.

---

### Day 1: Upper Body Strength & Postural Foundations
- **Warm-up (5-10 mins):** Arm circles (60 sec forward & back), band pull-aparts (2 sets of 15), light push-ups (10 reps), thoracic spine rotations.
- **Main Workout:**
  1. Barbell / Dumbbell Bench Press: 3 sets of 8-12 reps
  2. Lat Pulldowns or Assisted Pull-ups: 3 sets of 10-12 reps
  3. Overhead Dumbbell Shoulder Press: 3 sets of 10-12 reps
  4. Chest-Supported Dumbbell Rows: 3 sets of 12 reps
  5. Dumbbell Bicep Curls superset with Tricep Rope Pushdowns: 3 sets of 12-15 reps
- **Cooldown:** Shoulder cross-arm stretches, door-frame chest opener, dynamic neck rolls (hold each 30 sec).

---

### Day 2: Lower Body Power & Core Stabilization
- **Warm-up (5-10 mins):** Bodyweight air squats (15 reps), dynamic walking lunges (10 per leg), glute bridges (15 reps), hip mobility openers.
- **Main Workout:**
  1. Goblet Squats or Barbell Back Squats: 4 sets of 8-10 reps
  2. Romanian Deadlifts (Dumbbell or Barbell): 3 sets of 10-12 reps
  3. Bulgarian Split Squats: 3 sets of 10 reps per leg
  4. Standing Calf Raises: 3 sets of 15-20 reps
  5. Hanging Knee Raises / Forearm Plank: 3 sets of 45-60 sec hold
- **Cooldown:** Standing quad stretch, seated hamstring reach, child's pose (hold each 30 sec).

---

### Day 3: High-Intensity Interval Training (HIIT) & Functional Agility
- **Warm-up (5-10 mins):** Light jog or stationary cycling, high knees, butt kicks, torso twists.
- **Main Workout:**
  1. Kettlebell Swings: 4 rounds of 40 seconds work / 20 seconds rest
  2. Mountain Climbers: 4 rounds of 40 seconds work / 20 seconds rest
  3. Dumbbell Thrusters: 4 rounds of 40 seconds work / 20 seconds rest
  4. Battle Ropes or Shadow Boxing: 4 rounds of 40 seconds work / 20 seconds rest
  5. Russian Twists with weight: 3 sets of 20 reps total
- **Cooldown:** Full-body static stretches, deep diaphragmatic belly breathing (5 mins).

---

### Day 4: Active Recovery, Mobility & Flexibility
- **Warm-up (5 mins):** Cat-Cow spinal flows, downward-facing dog transitions.
- **Main Workout:**
  1. 30-45 Minute brisk outdoor power walk or gentle swimming
  2. Foam rolling: quads, upper back (thoracic), lats, and calves (60 sec per zone)
  3. Yoga flow sequence focusing on hip and shoulder mobility (20 mins)
- **Cooldown:** Reclined spinal twist, savasana rest (5 mins).

---

### Day 5: Push-Pull Hypertrophy & Density
- **Warm-up (5-10 mins):** Jumping jacks, inchworms, light resistance band chest press and rows.
- **Main Workout:**
  1. Incline Dumbbell Press: 3 sets of 10-12 reps
  2. Seated Cable Rows: 3 sets of 10-12 reps
  3. Dumbbell Lateral Raises: 4 sets of 12-15 reps
  4. Incline Dumbbell Hammer Curls: 3 sets of 12 reps
  5. Dips or Overhead Tricep Extension: 3 sets of 12-15 reps
  6. Abdominal Hanging Leg Raises: 3 sets of 12 reps
- **Cooldown:** Triceps overhead stretch, lat door stretch, wrist mobility.

---

### Day 6: Posterior Chain, Legs & Core Burnout
- **Warm-up (5-10 mins):** Hip airplanes, leg swings (front-to-back, side-to-side), bodyweight good mornings.
- **Main Workout:**
  1. Barbell or Trap Bar Deadlift: 3 sets of 6-8 reps
  2. Leg Press or Hack Squat: 3 sets of 10-12 reps
  3. Hamstring Swiss Ball Curls: 3 sets of 12-15 reps
  4. Walking Lunges: 3 sets of 12 steps per leg
  5. Cable Woodchoppers: 3 sets of 15 reps each side
- **Cooldown:** Pigeon pose, cobra pose, butterfly seated stretch.

---

### Day 7: Full Rest, Restoration & Weekly Preparation
- **Activities:**
  - Complete rest from intense mechanical loading.
  - Optional 20-minute light nature walk.
  - Review nutrition log, prepare healthy meals for the upcoming week, and aim for 8+ hours of quality sleep.
- **Recovery Tip:** Take a warm Epsom salt bath or contrast shower to promote systemic muscular blood flow."""


def generate_workout_gemini(user_input: dict) -> str:
    """
    Implements the core logic to generate a personalized 7-day workout plan
    using user inputs such as goal and intensity. Calls Google Gemini 1.5 Pro.
    """
    goal = user_input.get("goal", "general fitness")
    intensity = user_input.get("intensity", "medium")
    username = user_input.get("username") or user_input.get("name", "User")
    age = user_input.get("age", 25)
    weight = user_input.get("weight", 70)

    prompt = f"""You are a professional fitness trainer.

Create a personalized, structured 7-day workout plan for {username} (Age: {age}, Weight: {weight}kg) with the primary goal of **{goal}**, and who prefers **{intensity}** intensity workouts.

Each day must include:
- A warm-up (5-10 mins)
- Main workout (targeted exercises, sets & reps)
- Cooldown or recovery tip

Format:
Day 1:
Warm-up: ...
Main Workout: ...
Cooldown: ...
(Repeat for Day 2-7)

Make sure the plan is encouraging, scientifically grounded, and formatted clearly with markdown."""

    if genai_configured:
        try:
            import google.generativeai as genai
            model = genai.GenerativeModel(MODEL_NAME)
            response = model.generate_content(prompt)
            if response and response.text:
                return response.text.strip()
        except Exception as e:
            print(f"Gemini API workout generation encountered an error: {e}. Utilizing fallback generator.")
            return _generate_fallback_plan(goal, intensity)

    return _generate_fallback_plan(goal, intensity)
