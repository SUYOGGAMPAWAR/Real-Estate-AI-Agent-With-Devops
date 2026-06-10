from fastapi import FastAPI, Request, Form, Response
from fastapi.staticfiles import StaticFiles
from openai import AsyncOpenAI
from gtts import gTTS
import httpx
import os
import uvicorn
import uuid

app = FastAPI(title="AI Real Estate Automation Engine")

# Create a static folder to host the audio files
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize the AI Client via Groq
client = AsyncOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"), 
    base_url="https://api.groq.com/openai/v1"
)

SYSTEM_PROMPT = """
You are a highly professional real estate qualification assistant for a top brokerage in Maharashtra. 
Your job is to qualify incoming WhatsApp leads. 

You must extract three pieces of information:
1. Preferred Location (e.g., Akurdi, Wakad, Talegaon)
2. Property Size (e.g., 2 BHK, 3 BHK, Penthouse)
3. Budget

If the user provides all three, politely let them know an agent will call them within 1 minute with the best listings. 
If they are missing any of these details, politely ask ONE clarifying question to gather the missing info.
Keep responses short, friendly, and formatted for a text or voice message.
"""

@app.post("/webhook/whatsapp")
async def receive_whatsapp_message(
    request: Request,
    From: str = Form(...), 
    Body: str = Form(""), 
    NumMedia: int = Form(0),
    MediaUrl0: str = Form(None)
):
    sender = From
    user_message = Body
    print(f"Incoming WhatsApp from {sender}. Contains {NumMedia} media files.")

    try:
        # Handle Voice Notes via Whisper
        if NumMedia > 0 and MediaUrl0:
            print("Downloading and transcribing voice note...")
            audio_filepath = f"static/incoming_{uuid.uuid4().hex}.ogg"
            
            async with httpx.AsyncClient() as http_client:
                audio_response = await http_client.get(MediaUrl0, follow_redirects=True)
                with open(audio_filepath, "wb") as f:
                    f.write(audio_response.content)
            
            with open(audio_filepath, "rb") as f:
                transcription = await client.audio.transcriptions.create(
                    file=f,
                    model="whisper-large-v3"
                )
            user_message = transcription.text
            print(f"Transcribed Text: {user_message}")

        # Generate AI Response via Llama 3
        response = await client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7
        )
        ai_reply = response.choices[0].message.content
        print(f"AI Reply: {ai_reply}")

        # If it was a voice note, reply with an Audio file (gTTS)
        if NumMedia > 0:
            tts = gTTS(text=ai_reply, lang='en', tld='co.in')
            audio_filename = f"reply_{uuid.uuid4().hex}.mp3"
            tts.save(f"static/{audio_filename}")
            
            base_url = str(request.base_url).rstrip("/")
            media_reply_url = f"{base_url}/static/{audio_filename}"
            
            xml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
            <Response>
                <Message><Media>{media_reply_url}</Media></Message>
            </Response>"""
            return Response(content=xml_response, media_type="application/xml")
        
        # If it was a text message, reply with Text
        else:
            xml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
            <Response><Message>{ai_reply}</Message></Response>"""
            return Response(content=xml_response, media_type="application/xml")

    except Exception as e:
        print(f"Error: {e}")
        return Response(
            content='<?xml version="1.0" encoding="UTF-8"?><Response><Message>System Offline. Please try again later.</Message></Response>', 
            media_type="application/xml"
        )

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
            xml_response += '<Gather input="speech" action="/webhook/voice" speechTimeout="auto">'
            xml_response += f'<Say voice="Polly.Matthew-Neural">{ai_reply}</Say>'
            xml_response += '</Gather>'
        except Exception as e:
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