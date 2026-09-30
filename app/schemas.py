from pydantic import BaseModel, Field
from typing import Optional


class UserInput(BaseModel):
    user_id: int = Field(..., description="Unique User ID", example=101)
    username: str = Field(..., description="Full name or username", example="Alex Hunter")
    age: int = Field(..., ge=10, le=120, description="Age in years", example=25)
    weight: float = Field(..., gt=20, le=400, description="Weight in kg", example=72.5)
    goal: str = Field(..., description="Fitness goal (e.g., Weight Loss, Muscle Gain)", example="Weight Loss")
    intensity: str = Field(..., description="Intensity level (low, medium, high)", example="medium")


class WorkoutRequest(BaseModel):
    goal: str = Field(..., example="muscle gain")
    intensity: str = Field(..., example="high")


class FeedbackRequest(BaseModel):
    feedback: str = Field(..., example="Include more core exercises and one extra active rest day.")


class NutritionTipRequest(BaseModel):
    goal: str = Field(..., example="weight loss")


class PlanResponse(BaseModel):
    message: str
    workout_plan: str
    nutrition_tip: Optional[str] = None


class FeedbackResponse(BaseModel):
    message: str
    user_id: int
    updated_plan: str
