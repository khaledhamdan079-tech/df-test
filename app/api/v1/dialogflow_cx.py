from fastapi import APIRouter, Request
import requests

router = APIRouter(tags=["dialogflow_cx"])


BASE_URL = "https://dialogflow.googleapis.com/v3"

API_KEY = '6b5f927cd73172b839941f53d4ffc34d9c3e6689'
PROJECT_ID = "your-project-id"
LOCATION = "global"
AGENT_ID = "your-agent-id"
SESSION_ID = "default-session"

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}",
}


@router.post("/detect-intent")
async def detect_intent(request: Request):
    data = await request.json()
    print(data)
    # call the dialogflow cx api
    response = requests.post(
        f"{BASE_URL}/projects/{PROJECT_ID}/locations/{LOCATION}/agents/{AGENT_ID}/sessions/{SESSION_ID}/detectIntent",
        headers=HEADERS,
        json=data,
    )
    return response.json()
