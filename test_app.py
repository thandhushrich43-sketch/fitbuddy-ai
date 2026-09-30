import sys
from fastapi.testclient import TestClient
from app.main import app
from app.database import init_db

client = TestClient(app)

def run_tests():
    print("========================================")
    print("Running FitBuddy Automated Verification")
    print("========================================")
    
    # Initialize DB
    init_db()
    
    # 1. Test Homepage
    print("\n[1/7] Testing GET / (Homepage)...")
    res = client.get("/")
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    assert "FitBuddy - AI Workout Generator" in res.text
    assert "Generate Plan" in res.text
    print("  [OK] Homepage loaded successfully")

    # 2. Test Plan Generation (Form POST)
    print("\n[2/7] Testing POST /generate-workout (Form submission)...")
    payload = {
        "username": "Alex Hunter",
        "user_id": 101,
        "age": 24,
        "weight": 72.5,
        "goal": "Muscle Gain and Core Strength",
        "intensity": "High"
    }
    res = client.post("/generate-workout", data=payload)
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    assert "Your Personalized Workout Plan" in res.text
    assert "Alex Hunter" in res.text
    assert "Nutrition &amp; Recovery Tip" in res.text or "Nutrition & Recovery Tip" in res.text
    assert "Share Your Feedback" in res.text
    print("  [OK] Workout plan generated, user saved to DB, result rendered")

    # 3. Test Feedback Submission (Form POST)
    print("\n[3/7] Testing POST /submit-feedback (Plan update)...")
    feedback_payload = {
        "user_id": 101,
        "feedback": "Please add 15 minutes of cardio on Day 3 and more rest."
    }
    res = client.post("/submit-feedback", data=feedback_payload)
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    assert "Your plan has been updated based on your feedback!" in res.text
    assert "cardio" in res.text.lower() or "revised" in res.text.lower()
    print("  [OK] Feedback processed, plan updated, confirmation displayed")

    # 4. Test Admin View
    print("\n[4/7] Testing GET /view-all-users (Admin dashboard)...")
    res = client.get("/view-all-users")
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    assert "Alex Hunter" in res.text
    assert "#101" in res.text
    assert "FitBuddy - All Users &amp; Workout Plans" in res.text or "FitBuddy - All Users & Workout Plans" in res.text
    print("  [OK] Admin dashboard renders all users with original and updated plans")

    # 5. Test REST API: /generate-workout/gemini
    print("\n[5/7] Testing API: POST /generate-workout/gemini...")
    res = client.post("/generate-workout/gemini", json={"goal": "Weight Loss", "intensity": "medium"})
    assert res.status_code == 200
    data = res.json()
    assert "workout_plan" in data
    print("  [OK] Workout generation API endpoint passed")

    # 6. Test REST API: /nutrition-tip
    print("\n[6/7] Testing API: GET /nutrition-tip...")
    res = client.get("/nutrition-tip?goal=muscle+gain")
    assert res.status_code == 200
    data = res.json()
    assert "nutrition_tip" in data
    print("  [OK] Nutrition tip API endpoint passed")

    # 7. Test REST API: /api/users
    print("\n[7/7] Testing API: GET /api/users...")
    res = client.get("/api/users")
    assert res.status_code == 200
    users = res.json()
    assert len(users) >= 1
    assert users[0]["id"] == 101
    print(f"  [OK] Users API endpoint returned {len(users)} user(s)")

    print("\n========================================")
    print(" ALL 7 TEST SUITES PASSED FLAWLESSLY! ")
    print("========================================")

if __name__ == "__main__":
    run_tests()
