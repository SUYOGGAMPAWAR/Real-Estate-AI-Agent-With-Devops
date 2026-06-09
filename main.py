from fastapi import FastAPI, Request
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="AI Real Estate Automation Engine")

# This will later hold your OpenAI and Google Sheets logic
class WhatsAppMessage(BaseModel):
    sender: str
    message_body: str

@app.post("/webhook/whatsapp")
async def receive_whatsapp_message(request: Request):
    """
    This endpoint catches messages sent to your WhatsApp Business API.
    """
    payload = await request.json()
    
    # Extracting the message (simplified for demonstration)
    sender = payload.get("sender", "unknown")
    message = payload.get("message_body", "").lower()

    print(f"Incoming message from {sender}: {message}")

    # Preliminary routing logic before hitting the LLM
    target_locations = ["wakad", "talegaon", "akurdi"]
    property_types = ["2 bhk", "3 bhk", "penthouse"]

    location_match = any(loc in message for loc in target_locations)
    type_match = any(ptype in message for ptype in property_types)

    if location_match or type_match:
        # Here we will trigger the AI Agent to craft a personalized response
        # and ask if we can trigger the automated calling API.
        response_status = "AI Agent Triggered - Lead is qualified."
    else:
        # Fallback for general inquiries
        response_status = "General AI Response Triggered."

    return {"status": "success", "action_taken": response_status}

@app.get("/health")
def health_check():
    return {"status": "Engine is running perfectly"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)