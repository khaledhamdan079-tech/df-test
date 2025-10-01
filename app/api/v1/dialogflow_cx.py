from fastapi import APIRouter, Request
import requests
from pydantic import BaseModel, Field

router = APIRouter(tags=["dialogflow_cx"])


BASE_URL = "https://dialogflow.googleapis.com/v3"

API_KEY = '6b5f927cd73172b839941f53d4ffc34d9c3e6689'
PROJECT_ID = "apt-aleph-471911-k3"
LOCATION = "us-central1"
AGENT_ID = "e4926e9e-ddd0-4f04-9ba9-a3e1afe8d88b"
SESSION_ID = "default-session"

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}",
}

#let body has text and languageCode and make them required and let them show in the docs  and make them as required in the docs and swagger ui
class DetectIntentRequest(BaseModel):
    text: str = Field(..., description="The text to detect intent for")
    languageCode: str = Field(..., description="The language code to detect intent for")

@router.post("/detect-intent")
async def detect_intent(body: DetectIntentRequest):
    # call the dialogflow cx api
    response = requests.post(
        f"{BASE_URL}/projects/{PROJECT_ID}/locations/{LOCATION}/agents/{AGENT_ID}/sessions/{SESSION_ID}/detectIntent",
        headers=HEADERS,
        json={"queryInput": {"text": {"text": body.text, "languageCode": body.languageCode}}},
    )
    return response.json()