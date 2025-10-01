from fastapi import APIRouter, Request, HTTPException
import requests
from pydantic import BaseModel, Field
import logging

router = APIRouter(tags=["dialogflow_cx"])


BASE_URL = "https://dialogflow.googleapis.com/v3"

API_KEY = '6b5f927cd73172b839941f53d4ffc34d9c3e6689'
PROJECT_ID = "apt-aleph-471911-k3"
LOCATION = "us-central1"
AGENT_ID = "e4926e9e-ddd0-4f04-9ba9-a3e1afe8d88b"
SESSION_ID = "default-session"

HEADERS = {
    "Content-Type": "application/json",
}

#let body has text and languageCode and make them required and let them show in the docs  and make them as required in the docs and swagger ui
class DetectIntentRequest(BaseModel):
    text: str = Field(..., description="The text to detect intent for")
    languageCode: str = Field(..., description="The language code to detect intent for")

@router.post("/detect-intent")
async def detect_intent(body: DetectIntentRequest):
    # call the dialogflow cx api
    try:
        response = requests.post(
            f"{BASE_URL}/projects/{PROJECT_ID}/locations/{LOCATION}/agents/{AGENT_ID}/sessions/{SESSION_ID}:detectIntent?key={API_KEY}",
            headers=HEADERS,
            json={"queryInput": {"text": {"text": body.text, "languageCode": body.languageCode}}},
        )
        
        # Check if the request was successful
        response.raise_for_status()
        
        # Check if response has content
        if not response.text.strip():
            logging.error("Empty response from Dialogflow API")
            raise HTTPException(status_code=500, detail="Empty response from Dialogflow API")
        
        # Try to parse JSON
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError as e:
            logging.error(f"Failed to parse JSON response: {e}")
            logging.error(f"Response content: {response.text}")
            raise HTTPException(status_code=500, detail=f"Invalid JSON response from Dialogflow API: {response.text}")
            
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to connect to Dialogflow API: {str(e)}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")