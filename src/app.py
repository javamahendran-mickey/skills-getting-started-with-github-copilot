"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
static_dir = os.path.join(Path(__file__).parent, "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Volleyball": {
        "description": "Practice team drills and play friendly matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 18,
        "participants": ["maria@mergington.edu"]
    },
    "Track and Field": {
        "description": "Train for sprints, jumps, and relays",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 25,
        "participants": ["alex@mergington.edu"]
    },
    "Art Club": {
        "description": "Explore painting, drawing, and mixed media",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["nina@mergington.edu"]
    },
    "Drama Workshop": {
        "description": "Learn acting, improv, and stagecraft",
        "schedule": "Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 12,
        "participants": ["liam@mergington.edu"]
    },
    "Science Olympiad": {
        "description": "Prepare for science competitions and hands-on labs",
        "schedule": "Tuesdays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["sara@mergington.edu"]
    },
    "Debate Team": {
        "description": "Build public speaking and critical thinking skills",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["jordan@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, request: Request):
    """Sign up a student for an activity. Preserve special characters in the
    `email` query parameter (e.g. plus signs) by parsing the raw query string
    instead of relying on the default form-style decoding which converts
    '+' to space.
    """
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Parse raw query string to preserve '+' characters
    import urllib.parse
    qs = request.scope.get("query_string", b"").decode()
    email = None
    for part in qs.split("&"):
        if not part:
            continue
        key_value = part.split("=", 1)
        if len(key_value) == 2 and key_value[0] == "email":
            email = urllib.parse.unquote(key_value[1])
            break

    if not email:
        raise HTTPException(status_code=400, detail="Email query parameter is required")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student already signed up for this activity")

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/participants/{email}")
def remove_participant(activity_name: str, email: str):
    """Remove a participant from an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate participant is signed up
    if email not in activity["participants"]:
        raise HTTPException(status_code=400, detail="Participant not found in this activity")
    
    # Remove participant
    activity["participants"].remove(email)
    return {"message": f"Removed {email} from {activity_name}"}
