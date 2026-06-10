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

# Webhook 1: Handling WhatsApp Traffic
@app.post("/webhook/whatsapp")
async def receive_whatsapp_message(From: str = Form(...), Body: str = Form(...)):
    sender = From
    user_message = Body

    print(f"Incoming WhatsApp message from {sender}: {user_message}")

    try:
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

# Webhook 2: Handling Voice Call Traffic
@app.post("/webhook/voice")
async def receive_voice_call(request: Request):
    form_data = await request.form()
    user_speech = form_data.get("SpeechResult", "")

    xml_response = '<?xml version="1.0" encoding="UTF-8"?><Response>'

    if user_speech:
        print(f"Caller said: {user_speech}")
        try:
            response = await client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT + " Keep your answer under 2 sentences so it sounds natural on a phone call."},
                    {"role": "user", "content": user_speech}
                ],
                temperature=0.7
            )
            ai_reply = response.choices[0].message.content
            print(f"AI Voice Reply: {ai_reply}")

            xml_response += f'<Say voice="Polly.Matthew-Neural">{ai_reply}</Say>'
            xml_response += '<Gather input="speech" action="/webhook/voice" speechTimeout="auto"></Gather>'

        except Exception as e:
            print(f"Error: {e}")
            xml_response += '<Say>Sorry, my connection dropped. Please try again.</Say>'
    else:
        xml_response += '<Gather input="speech" action="/webhook/voice" speechTimeout="auto">'
        xml_response += '<Say voice="Polly.Matthew-Neural">Hello! I am the AI real estate assistant. What kind of property in Maharashtra are you looking for today?</Say>'
        xml_response += '</Gather>'

    xml_response += '</Response>'
    return Response(content=xml_response, media_type="application/xml")

@app.get("/health")
def health_check():
    return {"status": "AI Engine is running with live Twilio integration."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)