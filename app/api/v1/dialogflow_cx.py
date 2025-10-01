from fastapi import APIRouter, Request, HTTPException
import requests
from pydantic import BaseModel, Field
import logging
import os
import base64
import json
import tempfile
from google.auth.transport.requests import Request as GoogleRequest
from google.oauth2 import service_account

router = APIRouter(tags=["dialogflow_cx"])


BASE_URL = "https://dialogflow.googleapis.com/v3"

PROJECT_ID = "apt-aleph-471911-k3"
LOCATION = "us-central1"
AGENT_ID = "e4926e9e-ddd0-4f04-9ba9-a3e1afe8d88b"
SESSION_ID = "default-session"

# Service account credentials - supports both file path and base64 encoded JSON
SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
SERVICE_ACCOUNT_JSON_B64 = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON_B64")
SCOPES = ['https://www.googleapis.com/auth/cloud-platform']

def get_access_token():
    """Get OAuth2 access token using service account credentials"""
    try:
        if SERVICE_ACCOUNT_JSON_B64:
            # For Railway deployment - decode base64 JSON
            service_account_json = base64.b64decode(SERVICE_ACCOUNT_JSON_B64).decode('utf-8')
            service_account_info = json.loads(service_account_json)
            credentials = service_account.Credentials.from_service_account_info(
                service_account_info, scopes=SCOPES
            )
        elif SERVICE_ACCOUNT_FILE:
            # For local development - use file path
            credentials = service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, scopes=SCOPES
            )
        else:
            raise HTTPException(
                status_code=500, 
                detail="Neither GOOGLE_APPLICATION_CREDENTIALS nor GOOGLE_SERVICE_ACCOUNT_JSON_B64 environment variable is set"
            )
        
        credentials.refresh(GoogleRequest())
        return credentials.token
    except Exception as e:
        logging.error(f"Failed to get access token: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to authenticate with Google Cloud: {str(e)}"
        )

#let body has text and languageCode and make them required and let them show in the docs  and make them as required in the docs and swagger ui
class DetectIntentRequest(BaseModel):
    text: str = Field(..., description="The text to detect intent for")
    languageCode: str = Field(..., description="The language code to detect intent for")

@router.post("/detect-intent")
async def detect_intent(body: DetectIntentRequest):
    # call the dialogflow cx api
    try:
        # Get OAuth2 access token
        access_token = get_access_token()
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }
        
        response = requests.post(
            f"{BASE_URL}/projects/{PROJECT_ID}/locations/{LOCATION}/agents/{AGENT_ID}/sessions/{SESSION_ID}:detectIntent",
            headers=headers,
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