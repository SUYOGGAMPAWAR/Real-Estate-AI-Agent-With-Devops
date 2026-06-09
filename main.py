from fastapi import FastAPI, Request
from pydantic import BaseModel
from openai import AsyncOpenAI
import os
import uvicorn

app = FastAPI(title="AI Real Estate Automation Engine")

# Initialize the OpenAI Client
# It automatically looks for the OPENAI_API_KEY environment variable
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class WhatsAppMessage(BaseModel):
    sender: str
    message_body: str

# The System Prompt: This dictates exactly how your AI behaves
SYSTEM_PROMPT = """
You are a highly professional real estate qualification assistant for a top brokerage in Maharashtra. 
Your job is to qualify incoming WhatsApp leads. 

You must extract three pieces of information:
1. Preferred Location (e.g., Akurdi, Wakad, Talegaon)
2. Property Size (e.g., 2 BHK, 3 BHK, Penthouse)
3. Budget

If the user provides all three, politely let them know an agent will call them within 1 minute with the best listings. 
If they are missing any of these details, politely ask ONE clarifying question to gather the missing info.
Keep responses short, friendly, and formatted for WhatsApp.
"""

@app.post("/webhook/whatsapp")
async def receive_whatsapp_message(request: Request):
    payload = await request.json()
    
    sender = payload.get("sender", "unknown")
    user_message = payload.get("message_body", "")

    print(f"Incoming message from {sender}: {user_message}")

    try:
        # Call OpenAI to generate a dynamic response based on the lead's message
        response = await client.chat.completions.create(
            model="gpt-4o", # You can change this to gpt-3.5-turbo to save costs
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7
        )
        
        ai_reply = response.choices[0].message.content

        # Here is where we would normally trigger the WhatsApp API to send ai_reply back to the user
        print(f"AI Response to {sender}: {ai_reply}")

        return {"status": "success", "ai_response": ai_reply}

    except Exception as e:
        print(f"Error calling OpenAI: {e}")
        return {"status": "error", "message": "Failed to connect to AI brain."}

@app.get("/health")
def health_check():
    return {"status": "AI Engine is running with OpenAI integration."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)