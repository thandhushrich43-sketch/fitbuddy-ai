import os
from fastapi import APIRouter, Request, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import (
    SessionLocal,
    User,
    WorkoutPlan,
    save_user,
    save_plan,
    update_plan,
    get_original_plan,
    get_user,
    delete_user
)
from app.schemas import UserInput, WorkoutRequest, FeedbackRequest
from app.gemini_generator import generate_workout_gemini
from app.gemini_flash_generator import generate_nutrition_tip_with_flash
from app.updated_plan import update_workout_plan

router = APIRouter()

# Setup templates directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
templates = Jinja2Templates(directory=TEMPLATE_DIR)


# -------------------------------------------------------------
# Frontend HTML Routes (Jinja2 Rendered)
# -------------------------------------------------------------

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """
    Renders the homepage form (index.html) to collect user fitness profile.
    """
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


@router.post("/generate-workout", response_class=HTMLResponse)
async def generate_workout_form(
    request: Request,
    username: str = Form(...),
    user_id: int = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...)
):
    """
    Handles form submission from index.html:
    1. Generates 7-day workout plan using Gemini 1.5 Pro
    2. Generates practical nutrition tip using Gemini Flash
    3. Persists user profile and generated plan into SQLite
    4. Renders result.html with personalized details
    """
    try:
        # Prepare payload for workout generation
        user_input = {
            "username": username,
            "user_id": user_id,
            "age": age,
            "weight": weight,
            "goal": goal,
            "intensity": intensity
        }

        # 1. AI Generation
        workout_plan = generate_workout_gemini(user_input)
        nutrition_tip = generate_nutrition_tip_with_flash(goal)

        # 2. Database Storage
        save_user(
            user_id=user_id,
            name=username,
            age=age,
            weight=weight,
            goal=goal,
            intensity=intensity
        )
        save_plan(user_id=user_id, plan=workout_plan)

        # 3. Render Result Page
        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "username": username,
                "user_id": user_id,
                "age": age,
                "weight": weight,
                "goal": goal,
                "intensity": intensity,
                "workout_plan": workout_plan,
                "nutrition_tip": nutrition_tip,
                "feedback_message": None
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating workout plan: {str(e)}")


@router.post("/submit-feedback", response_class=HTMLResponse)
async def submit_feedback_form(
    request: Request,
    user_id: int = Form(...),
    feedback: str = Form(...)
):
    """
    Handles feedback submission from result.html:
    1. Fetches original plan and user profile from SQLite
    2. Sends plan + feedback to Gemini 1.5 Pro for dynamic refinement
    3. Updates database with revised plan
    4. Renders result.html displaying the refined plan and confirmation banner
    """
    user = get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found. Please generate a plan first.")

    original_plan = get_original_plan(user_id)
    if not original_plan:
        raise HTTPException(status_code=404, detail="Original plan not found for this user.")

    # Generate updated plan via AI
    updated_plan_text = update_workout_plan(original_plan, feedback)
    update_plan(user_id, updated_plan_text)

    # Fresh nutrition tip based on user's goal
    nutrition_tip = generate_nutrition_tip_with_flash(user.goal)

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "username": user.name,
            "user_id": user.id,
            "age": user.age,
            "weight": user.weight,
            "goal": user.goal,
            "intensity": user.intensity,
            "workout_plan": updated_plan_text,
            "original_plan": original_plan,
            "nutrition_tip": nutrition_tip,
            "feedback_message": "Your plan has been updated based on your feedback!"
        }
    )


@router.get("/view-all-users", response_class=HTMLResponse)
async def view_all_users_page(request: Request):
    """
    Admin dashboard displaying all registered users, their parameters,
    and their original vs updated workout plans in a clean responsive table.
    """
    db = SessionLocal()
    try:
        users = db.query(User).all()
        user_data = []
        for user in users:
            plan = db.query(WorkoutPlan).filter(WorkoutPlan.user_id == user.id).first()
            user_data.append({
                "id": user.id,
                "name": user.name,
                "age": user.age,
                "weight": user.weight,
                "goal": user.goal,
                "intensity": user.intensity,
                "original_plan": plan.original_plan if plan else "N/A",
                "updated_plan": plan.updated_plan if (plan and plan.updated_plan) else "Not updated"
            })
        return templates.TemplateResponse(
            request=request,
            name="all_users.html",
            context={
                "users": user_data
            }
        )
    finally:
        db.close()


@router.post("/delete-user/{user_id}")
async def delete_user_route(user_id: int):
    """
    Deletes a user and their associated plans from SQLite database.
    """
    deleted = delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return RedirectResponse(url="/view-all-users", status_code=303)


# -------------------------------------------------------------
# REST API Endpoints (as defined in Documentation Milestones)
# -------------------------------------------------------------

# 1. API: Generate workout using Gemini Pro
@router.post("/generate-workout/gemini")
async def generate_gemini_workout(request: WorkoutRequest):
    try:
        result = generate_workout_gemini({
            "goal": request.goal,
            "intensity": request.intensity
        })
        return {"model": "gemini-pro", "workout_plan": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 2. API: Generate nutrition tip using Gemini Flash
@router.get("/nutrition-tip")
def get_flash_tip(goal: str):
    tip = generate_nutrition_tip_with_flash(goal)
    return {"goal": goal, "nutrition_tip": tip}


# 3. API: Save user info & generate plan
@router.post("/generate-plan")
def generate_plan(user_data: UserInput):
    try:
        save_user(
            user_id=user_data.user_id,
            name=user_data.username,
            age=user_data.age,
            weight=user_data.weight,
            goal=user_data.goal,
            intensity=user_data.intensity
        )

        plan = generate_workout_gemini({
            "username": user_data.username,
            "goal": user_data.goal,
            "intensity": user_data.intensity,
            "age": user_data.age,
            "weight": user_data.weight
        })

        save_plan(user_data.user_id, plan)
        return {
            "message": "Workout plan generated and saved successfully!",
            "workout_plan": plan
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {str(e)}")


# 4. API: Update workout plan based on user feedback
@router.post("/update-plan/{user_id}")
def update_user_plan(user_id: int, data: FeedbackRequest):
    original = get_original_plan(user_id)
    if not original:
        return {"error": "Original plan not found for this user."}

    updated = update_workout_plan(original, data.feedback)
    update_plan(user_id, updated)
    return {"updated_plan": updated}


# 5. API: Get all users JSON
@router.get("/api/users")
def get_users_api():
    db = SessionLocal()
    try:
        users = db.query(User).all()
        result = []
        for user in users:
            plan = db.query(WorkoutPlan).filter(WorkoutPlan.user_id == user.id).first()
            result.append({
                "id": user.id,
                "name": user.name,
                "age": user.age,
                "weight": user.weight,
                "goal": user.goal,
                "intensity": user.intensity,
                "original_plan": plan.original_plan if plan else None,
                "updated_plan": plan.updated_plan if plan else None
            })
        return result
    finally:
        db.close()
