from fastapi import FastAPI, Request, Form, Response
from openai import AsyncOpenAI
import os
import uvicorn

app = FastAPI(title="AI Real Estate Automation Engine")

# Initialize the AI Client (Groq)
client = AsyncOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"), 
    base_url="https://api.groq.com/openai/v1"
)

# The System Prompt
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

# Notice we changed Request/JSON to Form data specifically for Twilio
@app.post("/webhook/whatsapp")
async def receive_whatsapp_message(From: str = Form(...), Body: str = Form(...)):
    
    # Twilio sends the sender's phone number in 'From' and the text in 'Body'
    sender = From
    user_message = Body

    print(f"Incoming WhatsApp message from {sender}: {user_message}")

    try:
        # Call Groq's Llama 3 model
        response = await client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7
        )
        
        ai_reply = response.choices[0].message.content
        print(f"AI Response to {sender}: {ai_reply}")

        # Twilio expects an XML response (called TwiML) to trigger the outgoing text
        xml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
        <Response>
            <Message>{ai_reply}</Message>
        </Response>"""
        
        return Response(content=xml_response, media_type="application/xml")

    except Exception as e:
        print(f"Error calling AI brain: {e}")
        error_xml = """<?xml version="1.0" encoding="UTF-8"?>
        <Response>
            <Message>System Offline. Please try again later.</Message>
        </Response>"""
        return Response(content=error_xml, media_type="application/xml")

@app.get("/health")
def health_check():
    return {"status": "AI Engine is running with live Twilio integration."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)