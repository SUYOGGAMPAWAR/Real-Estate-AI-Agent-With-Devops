# 🏢 AI Real Estate Automation Engine

An enterprise-grade, omnichannel AI agent built to automatically qualify real estate leads. This system integrates WhatsApp Text, WhatsApp Voice Notes, and Live Telephone Calls into a unified pipeline. It uses Groq's high-speed inference (Llama 3 & Whisper) and is deployed via a fully automated Jenkins CI/CD pipeline using Docker.

## 🚀 Key Features
* **Omnichannel Lead Capture:** Communicates via WhatsApp Text, WhatsApp Voice Notes, and Direct Phone Calls.
* **Intelligent Qualification:** Uses Llama-3.3-70b to extract Location, Budget, and Property Size natively, asking dynamic follow-up questions if data is missing.
* **Real-Time Voice Processing:** * *WhatsApp:* Downloads incoming audio, transcribes via Groq Whisper, and replies with localized Indian-English audio via gTTS.
  * *Live Calls:* Utilizes Twilio TwiML `<Gather>` tags for natural, human-like "barge-in" telephone conversations.
* **Secure DevOps Pipeline:** Jenkins CI/CD pipeline securely injects API credentials, builds isolated Docker containers, and manages deployments without exposing secrets.

## 🛠️ Tech Stack
* **Backend:** FastAPI, Python, Uvicorn
* **AI & Machine Learning:** Groq API, Meta Llama-3.3-70b, OpenAI Whisper
* **Communications:** Twilio WhatsApp Sandbox, Twilio Voice Webhooks
* **DevOps:** Docker, Docker Compose, Jenkins, Ngrok

---

## ⚙️ Step-by-Step Walkthrough & Setup

### Step 1: Clone the Repository
```bash
git clone [https://github.com/YOUR_USERNAME/Real-Estate-AI-Agent-With-Devops.git](https://github.com/YOUR_USERNAME/Real-Estate-AI-Agent-With-Devops.git)
cd Real-Estate-AI-Agent-With-Devops