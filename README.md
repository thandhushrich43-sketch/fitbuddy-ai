# 🏋️‍♂️ FitBuddy – AI Fitness Plan Generator using Gemini Models

FitBuddy is an intelligent, full-stack web application that uses Google’s Gemini Generative AI models to generate personalized 7-day workout plans and tailored nutrition/recovery tips. Built with **FastAPI**, **SQLAlchemy (SQLite)**, and **Jinja2**, FitBuddy simplifies the process of creating structured fitness routines and adapting them dynamically based on user feedback.

---

## 🌟 Key Features & Scenarios

1. **Personalized 7-Day Workout Routine:**
   - Takes user profile: Name, User ID, Age, Weight (kg), Fitness Goal, and Workout Intensity (Low, Medium, High).
   - Generates a day-wise regimen with Warm-ups, Main Workouts (exercises, sets, reps), and Cooldowns via **Gemini 1.5 Pro**.
2. **Dynamic AI Feedback Loop:**
   - Users can request alterations (e.g. *"add yoga"*, *"more focus on cardio"*, *"include more rest days"*).
   - The feedback is passed to **Gemini 1.5 Pro** to intelligently revise the plan while preserving the user's progress.
3. **Targeted Nutrition & Recovery Advice:**
   - Powered by **Gemini Flash** for fast, actionable dietary and recovery recommendations aligned with user goals.
4. **Admin / Trainer Dashboard (`/view-all-users`):**
   - Displays all registered clients, their physical parameters, and side-by-side comparison of **Original** vs **Updated** plans.
5. **Interactive Swagger API Documentation (`/docs`):**
   - Provides live interactive OpenAPI endpoints for all generation, feedback, and database queries.

---

## 📁 Project Directory Structure

```text
fit buddy/
│
├── requirements.txt            # Project Python dependencies
├── .env                        # Environment variables (Gemini API Key)
├── .env.example                # Example environment template
├── test_app.py                 # Automated test suite
├── README.md                   # Complete documentation & setup guide
│
├── app/
│   ├── __init__.py             # Package initializer
│   ├── main.py                 # FastAPI application entrypoint & static mounting
│   ├── routes.py               # Core web routes (HTML) and REST API endpoints
│   ├── database.py             # SQLite DB models & SQLAlchemy CRUD logic
│   ├── schemas.py              # Pydantic models for validation
│   ├── gemini_generator.py     # Gemini Pro 1.5 - 7-day workout plan generator
│   ├── gemini_flash_generator.py # Gemini Flash - quick nutrition/recovery tips
│   ├── updated_plan.py         # Gemini Pro - feedback-based workout plan updater
│   └── nutrition.py            # Nutrition calculations & macro guidelines
│
├── templates/
│   ├── index.html              # User input form homepage
│   ├── result.html             # Personalized plan, nutrition tip, feedback form
│   └── all_users.html          # Admin dashboard of all users & plans
│
├── static/
│   ├── css/
│   │   └── style.css           # Glassmorphism gym-themed styling & responsiveness
│   └── images/
│       └── gym-bg.jpg          # Gym background asset
│
└── fitbuddy.db                 # Local SQLite database (auto-generated)
```

---

## 🛠️ Step-by-Step VS Code Setup & Installation Guide

### Prerequisites
- [Visual Studio Code](https://code.visualstudio.com/)
- [Python 3.10+](https://www.python.org/downloads/) installed with "Add Python to PATH" checked.

### Step 1: Open the Project in VS Code
1. Open VS Code.
2. Select **File > Open Folder...** and choose the `fit buddy` folder.
3. Open the built-in terminal in VS Code using ``Ctrl + ` `` (or **Terminal > New Terminal**).

### Step 2: Create and Activate Virtual Environment

**On Windows (PowerShell):**
```powershell
python -m venv fitbuddy-env
.\fitbuddy-env\Scripts\activate
```

*(If you encounter execution policy restrictions on Windows PowerShell, run: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`)*

**On macOS / Linux:**
```bash
python3 -m venv fitbuddy-env
source fitbuddy-env/bin/activate
```

### Step 3: Install Required Dependencies
With the virtual environment activated:
```bash
pip install -r requirements.txt
```

---

## 🔑 Gemini API Key Configuration

1. Obtain a Google Gemini API Key for free at [Google AI Studio](https://aistudio.google.com/app/apikey).
2. Open the `.env` file in the root directory:
   ```env
   GOOGLE_API_KEY=AIzaSy...your_actual_key_here
   GEMINI_PRO_MODEL=gemini-1.5-pro
   GEMINI_FLASH_MODEL=gemini-1.5-flash
   ```
3. Save the file.
*(Note: If no API key is provided, the application runs seamlessly in smart offline demonstration mode, ensuring you can test UI and database workflows immediately).*

---

## 🚀 Running the Application

Start the FastAPI local development server using Uvicorn:

```bash
uvicorn app.main:app --reload
```

You should see output similar to:
```text
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Application startup complete.
```

---

## 🌐 Exploring the Application

| URL | Description |
| :--- | :--- |
| **`http://127.0.0.1:8000`** | **Home Page**: Enter your Name, ID, Age, Weight, Goal, and Intensity to generate your personalized 7-day routine. |
| **`http://127.0.0.1:8000/view-all-users`** | **Admin Dashboard**: Inspect all registered users, compare original vs feedback-updated plans, or remove profiles. |
| **`http://127.0.0.1:8000/docs`** | **Swagger UI**: Interactive REST API documentation to test endpoints directly. |

---

## 🧪 Automated Testing

To run the complete automated test verification suite verifying all 7 core functionalities:

```bash
python test_app.py
```

### Verified Test Cases:
- `GET /` — Renders home page form.
- `POST /generate-workout` — Generates 7-day workout plan and nutrition tip, saves to SQLite.
- `POST /submit-feedback` — Updates workout plan with feedback via Gemini Pro.
- `GET /view-all-users` — Verifies user data and dual plan display in admin dashboard.
- `POST /generate-workout/gemini` — Tests REST API Gemini workout generation.
- `GET /nutrition-tip` — Tests REST API Gemini Flash nutrition tip generation.
- `GET /api/users` — Tests REST API database querying.
"# fitbuddy-ai" 
