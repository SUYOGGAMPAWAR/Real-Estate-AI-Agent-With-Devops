# 🏢 Real Estate AI Automation Engine

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/FastAPI-0.100+-green?style=for-the-badge&logo=fastapi" />
  <img src="https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker" />
  <img src="https://img.shields.io/badge/Jenkins-CI%2FCD-D24939?style=for-the-badge&logo=jenkins" />
  <img src="https://img.shields.io/badge/Groq-LLaMA%203-FF6B35?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Twilio-WhatsApp%20%26%20Voice-F22F46?style=for-the-badge&logo=twilio" />
</p>

> An enterprise-grade, omnichannel AI agent that automatically qualifies real estate leads via **WhatsApp Text**, **WhatsApp Voice Notes**, and **Live Phone Calls** — all powered by Meta's Llama 3 on Groq and deployed through a fully automated Jenkins + Docker CI/CD pipeline.

---

## 📌 Table of Contents

1. [Project Overview](#-project-overview)
2. [Architecture](#-architecture)
3. [Key Features](#-key-features)
4. [Tech Stack](#-tech-stack)
5. [Prerequisites](#-prerequisites)
6. [Step 1 — Get Your API Keys](#step-1--get-your-api-keys)
7. [Step 2 — Clone & Configure the Project](#step-2--clone--configure-the-project)
8. [Step 3 — Run Locally (No Docker)](#step-3--run-locally-no-docker)
9. [Step 4 — Build & Run with Docker](#step-4--build--run-with-docker)
10. [Step 5 — Expose with Ngrok](#step-5--expose-with-ngrok)
11. [Step 6 — Configure Twilio WhatsApp Sandbox](#step-6--configure-twilio-whatsapp-sandbox)
12. [Step 7 — Configure Twilio Voice Webhook](#step-7--configure-twilio-voice-webhook)
13. [Step 8 — Set Up Jenkins CI/CD Pipeline](#step-8--set-up-jenkins-cicd-pipeline)
14. [Step 9 — Test End-to-End](#step-9--test-end-to-end)
15. [Project Structure](#-project-structure)
16. [How It Works](#-how-it-works)
17. [Troubleshooting](#-troubleshooting)
18. [Author](#-author)

---

## 🎯 Project Overview

This project is a **production-style AI backend** for a real estate brokerage in Maharashtra, India. It acts as an intelligent first-response agent that can handle inbound leads 24/7 via:

- 📱 **WhatsApp Text** — Responds instantly with AI-generated qualification questions
- 🎤 **WhatsApp Voice Notes** — Transcribes audio via Whisper, generates a reply, and sends back a human-like audio response
- 📞 **Live Phone Calls** — Conducts a real-time spoken conversation using Twilio TwiML

The AI agent extracts three key pieces of lead data — **Location**, **Property Size**, and **Budget** — and confirms that an agent will call back once all details are collected.

---

## 🏗️ Architecture

```
 User (WhatsApp / Phone Call)
        │
        ▼
  ┌─────────────┐
  │   TWILIO    │  ← Receives all inbound communication
  └──────┬──────┘
         │  HTTP Webhook (POST)
         ▼
  ┌──────────────────────────────────────┐
  │         FastAPI Backend              │
  │  ┌────────────┐  ┌────────────────┐  │
  │  │ /webhook/  │  │ /webhook/      │  │
  │  │ whatsapp   │  │ voice          │  │
  │  └─────┬──────┘  └───────┬────────┘  │
  │        │                 │           │
  │        ▼                 ▼           │
  │  ┌───────────────────────────────┐   │
  │  │         GROQ API              │   │
  │  │  Whisper (STT) + LLaMA 3 LLM  │   │
  │  └───────────────────────────────┘   │
  │        │                             │
  │        ▼                             │
  │   gTTS (Text-to-Speech)             │
  └──────────────────────────────────────┘
         │
         ▼
  ┌─────────────┐
  │   TWILIO    │  ← Sends AI reply back to user
  └─────────────┘

  DevOps Layer:
  ┌────────────────────────────────────────┐
  │  GitHub Push → Jenkins → Docker Build  │
  │  → docker-compose up -d (Live Deploy)  │
  │  → Ngrok tunnels localhost to Twilio   │
  └────────────────────────────────────────┘
```

---

## 🚀 Key Features

| Feature | Description |
|---|---|
| 💬 WhatsApp Text Handling | Receives text leads, generates AI responses via LLaMA 3 |
| 🎙️ Voice Note Transcription | Downloads OGG audio, transcribes using Groq Whisper |
| 🔊 Audio Reply Generation | Converts AI text to Indian-English audio via gTTS |
| 📞 Live Call Handling | Conducts real-time spoken conversations using TwiML `<Gather>` |
| 🧠 Lead Qualification Logic | Extracts Location, Budget, Property Size; asks follow-ups if missing |
| 🔐 Secure Secret Injection | Jenkins injects API keys at build time — no secrets in code |
| 🐳 Containerized Deployment | Entire app runs in an isolated Docker container |
| ♻️ CI/CD Automation | GitHub push triggers Jenkins pipeline to rebuild and redeploy |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend Framework** | FastAPI + Uvicorn |
| **Language** | Python 3.11 |
| **AI Model** | Meta LLaMA-3.3-70b via Groq API |
| **Speech-to-Text** | Groq Whisper Large v3 |
| **Text-to-Speech** | gTTS (Google Text-to-Speech, Indian English) |
| **Communication** | Twilio (WhatsApp Sandbox + Voice Webhooks) |
| **Containerization** | Docker + Docker Compose |
| **CI/CD** | Jenkins |
| **Tunneling (Dev)** | Ngrok |
| **HTTP Client** | httpx (async) |

---

## ✅ Prerequisites

Before you start, make sure you have the following accounts and tools ready:

### Accounts Required
- [ ] [Groq Cloud Account](https://console.groq.com) — Free tier available, for LLaMA 3 + Whisper API
- [ ] [Twilio Account](https://www.twilio.com/try-twilio) — Free trial works, for WhatsApp + Voice
- [ ] [Ngrok Account](https://ngrok.com) — Free tier available, for tunneling

### Tools Required (install on your machine)
- [ ] **Python 3.11+** — `python --version`
- [ ] **Docker & Docker Compose** — `docker --version && docker compose version`
- [ ] **Git** — `git --version`
- [ ] **Jenkins** — Running locally or on a VM (see [Jenkins Install Guide](https://www.jenkins.io/doc/book/installing/))
- [ ] **Ngrok CLI** — `ngrok --version`

---

## Step 1 — Get Your API Keys

### 1A. Groq API Key (for LLaMA 3 + Whisper)

1. Go to [https://console.groq.com](https://console.groq.com) and sign up or log in.
2. Navigate to **API Keys** in the left sidebar.
3. Click **Create API Key**, give it a name like `real-estate-agent`.
4. Copy and save the key — it starts with `gsk_...`

> ⚠️ **Note:** The `OPENAI_API_KEY` environment variable in this project actually holds your **Groq** API key. The app uses Groq's OpenAI-compatible endpoint — this is intentional.

### 1B. Twilio Credentials

1. Sign up at [https://www.twilio.com/try-twilio](https://www.twilio.com/try-twilio).
2. From the Twilio Console dashboard, note down:
   - **Account SID** (starts with `AC...`)
   - **Auth Token**
3. You will use these in the Twilio dashboard to configure webhooks (not in `.env` for this project).

---

## Step 2 — Clone & Configure the Project

### 2A. Clone the Repository

```bash
git clone https://github.com/SUYOGGAMPAWAR/Real-Estate-AI-Agent-With-Devops.git
cd Real-Estate-AI-Agent-With-Devops
```

### 2B. Create the `.env` File

Create a `.env` file in the root of the project directory:

```bash
touch .env
```

Open it and add your Groq API key:

```env
OPENAI_API_KEY=gsk_your_groq_api_key_here
```

> 🔒 This file is used by Docker Compose to inject the key as an environment variable. **Never commit this file to Git.** Add `.env` to your `.gitignore`.

### 2C. Verify `.gitignore`

Make sure `.env` is excluded from version control:

```bash
echo ".env" >> .gitignore
echo "static/" >> .gitignore
```

---

## Step 3 — Run Locally (No Docker)

Use this to quickly test the app without Docker during development.

### 3A. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
```

### 3B. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3C. Export the Environment Variable

```bash
export OPENAI_API_KEY=gsk_your_groq_api_key_here
# Windows: set OPENAI_API_KEY=gsk_your_groq_api_key_here
```

### 3D. Start the Server

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API is now live at: **`http://localhost:8000`**

You can verify the health check at: **`http://localhost:8000/health`**

Expected response:
```json
{"status": "AI Engine is running with live Twilio integration."}
```

---

## Step 4 — Build & Run with Docker

### 4A. Build the Docker Image

```bash
docker build -t real-estate-ai-backend:latest .
```

### 4B. Run Using Docker Compose

Make sure your `.env` file exists with your Groq API key, then:

```bash
docker compose up -d --build
```

This will:
- Build the image from the `Dockerfile`
- Start the container named `real_estate_ai_backend`
- Expose port `8000` on your host machine
- Mount the `./static/` folder so audio files persist across restarts

### 4C. Verify the Container is Running

```bash
docker ps
```

You should see `real_estate_ai_backend` running. Confirm it's healthy:

```bash
curl http://localhost:8000/health
```

### 4D. View Logs

```bash
docker logs real_estate_ai_backend -f
```

### 4E. Stop the Container

```bash
docker compose down
```

---

## Step 5 — Expose with Ngrok

Twilio needs a **publicly accessible URL** to send webhooks to your local machine. Ngrok creates a secure tunnel.

### 5A. Install Ngrok

```bash
# macOS (Homebrew)
brew install ngrok

# Linux / Windows
# Download from: https://ngrok.com/download
```

### 5B. Authenticate Ngrok (first time only)

```bash
ngrok config add-authtoken YOUR_NGROK_AUTH_TOKEN
```

Get your auth token from: [https://dashboard.ngrok.com/auth/your-authtoken](https://dashboard.ngrok.com/auth/your-authtoken)

### 5C. Start the Ngrok Tunnel

```bash
ngrok http 8000
```

Ngrok will display something like:

```
Forwarding  https://abc123xyz.ngrok-free.app -> http://localhost:8000
```

> 📋 **Copy the HTTPS URL** (e.g., `https://abc123xyz.ngrok-free.app`) — you will use this in Twilio's webhook configuration in the next steps.

> ⚠️ **Important:** The free tier of Ngrok generates a new URL each time you restart. You will need to update your Twilio webhooks whenever the URL changes. Upgrade to a paid plan to get a static domain.

---

## Step 6 — Configure Twilio WhatsApp Sandbox

This lets you test the WhatsApp integration using Twilio's sandbox (no need for a real WhatsApp Business account during development).

### 6A. Enable WhatsApp Sandbox

1. Log in to the [Twilio Console](https://console.twilio.com).
2. In the left sidebar, go to **Messaging → Try it out → Send a WhatsApp message**.
3. Follow the instructions to join the sandbox — you'll WhatsApp a join code to a Twilio number.

### 6B. Set the Webhook URL

1. Still in the Twilio Console, go to **Messaging → Settings → WhatsApp Sandbox Settings**.
2. Under **"When a message comes in"**, enter your Ngrok URL + the webhook path:

```
https://abc123xyz.ngrok-free.app/webhook/whatsapp
```

3. Set the method to **`HTTP POST`**.
4. Click **Save**.

### 6C. Test WhatsApp Text Message

Open WhatsApp on your phone and send a message to the Twilio sandbox number. You should receive an AI reply within a few seconds.

Try messages like:
- `"Hi, I'm looking for a property"`
- `"I want a 3 BHK in Wakad"`
- `"My budget is 80 lakhs, I want 2 BHK in Akurdi"`

### 6D. Test WhatsApp Voice Note

Record a voice message in WhatsApp and send it to the Twilio sandbox number. The agent will:
1. Download your OGG audio file
2. Transcribe it using Groq Whisper
3. Generate an AI text reply using LLaMA 3
4. Convert it to an Indian-English MP3 using gTTS
5. Send the audio file back to you on WhatsApp

---

## Step 7 — Configure Twilio Voice Webhook

This enables the AI to answer live phone calls.

### 7A. Get a Twilio Phone Number

1. In the Twilio Console, go to **Phone Numbers → Manage → Buy a Number**.
2. Select a number that supports **Voice** capability.
3. Purchase (free trial credits are sufficient).

### 7B. Set the Voice Webhook

1. Go to **Phone Numbers → Manage → Active Numbers**.
2. Click on your number.
3. Under **"A Call Comes In"**, set:
   - **Webhook URL:**
     ```
     https://abc123xyz.ngrok-free.app/webhook/voice
     ```
   - **HTTP Method:** `HTTP POST`
4. Click **Save**.

### 7C. Test the Voice Call

Call your Twilio phone number from any phone. You should hear the AI agent greet you and ask what kind of property you're looking for.

The call flow works as a continuous loop using TwiML `<Gather>`:
1. AI speaks a question
2. Waits for you to respond
3. Sends your speech to LLaMA 3
4. Speaks the AI's reply
5. Repeats until the call ends

---

## Step 8 — Set Up Jenkins CI/CD Pipeline

This automates the build and deployment process every time you push code to GitHub.

### 8A. Install and Start Jenkins

If Jenkins is not already running, follow the [official install guide](https://www.jenkins.io/doc/book/installing/). On Ubuntu:

```bash
# Install Java (required for Jenkins)
sudo apt install -y openjdk-17-jdk

# Add Jenkins repo and install
curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | sudo tee \
  /usr/share/keyrings/jenkins-keyring.asc > /dev/null

echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
  https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null

sudo apt-get update && sudo apt-get install -y jenkins
sudo systemctl start jenkins
sudo systemctl enable jenkins
```

Access Jenkins at `http://localhost:8080` and complete initial setup.

### 8B. Install Required Jenkins Plugins

Go to **Manage Jenkins → Plugins → Available** and install:

- **Git Plugin** — for `checkout scm`
- **Pipeline** — for Declarative Pipeline support
- **Docker Pipeline** — for Docker commands in pipeline stages
- **Credentials Binding Plugin** — for securely injecting API keys

### 8C. Add Your Groq API Key as a Jenkins Credential

> ⚠️ **Never hardcode API keys in your Jenkinsfile.** This step securely injects the key at runtime.

1. Go to **Manage Jenkins → Credentials → System → Global credentials → Add Credentials**.
2. Configure as follows:
   - **Kind:** Secret text
   - **Secret:** `gsk_your_groq_api_key_here`
   - **ID:** `openai-api-key` ← This must exactly match the Jenkinsfile
   - **Description:** Groq API Key for Real Estate AI Agent
3. Click **Create**.

### 8D. Create the Jenkins Pipeline Job

1. From the Jenkins dashboard, click **New Item**.
2. Enter name: `real-estate-ai-pipeline`
3. Select **Pipeline** and click **OK**.
4. Under **Pipeline → Definition**, select **Pipeline script from SCM**.
5. Set:
   - **SCM:** Git
   - **Repository URL:** `https://github.com/SUYOGGAMPAWAR/Real-Estate-AI-Agent-With-Devops.git`
   - **Branch:** `*/main` (or your default branch)
   - **Script Path:** `Jenkinsfile`
6. Click **Save**.

### 8E. Understanding the Jenkinsfile Stages

```
Stage 1: Code Checkout     → Pulls latest code from GitHub
Stage 2: Code Analysis     → Runs Python syntax check (compileall)
Stage 3: Build Docker Image → Builds real-estate-ai-backend:latest
Stage 4: Local Cleanup      → Prunes dangling Docker images
Stage 5: Deploy Locally     → Stops old container, runs docker-compose up -d
```

### 8F. Trigger the Pipeline

Click **Build Now** on your Jenkins job. Watch the **Console Output** to see each stage execute. After Stage 5, your updated container will be live.

### 8G. Set Up GitHub Webhook for Auto-Trigger (Optional)

To automatically trigger the Jenkins pipeline on every `git push`:

1. In your GitHub repository, go to **Settings → Webhooks → Add webhook**.
2. Set **Payload URL** to: `http://your-jenkins-ip:8080/github-webhook/`
3. Set **Content type** to `application/json`.
4. Select **Just the push event**.
5. Click **Add webhook**.

In Jenkins, under your job configuration, enable **"GitHub hook trigger for GITScm polling"**.

---

## Step 9 — Test End-to-End

### ✅ Health Check
```bash
curl http://localhost:8000/health
# Expected: {"status": "AI Engine is running with live Twilio integration."}
```

### ✅ Manual Webhook Test (Text)

Simulate a WhatsApp text message to test the AI locally before connecting Twilio:

```bash
curl -X POST http://localhost:8000/webhook/whatsapp \
  -d "From=whatsapp:+911234567890" \
  -d "Body=I want a 2 BHK in Wakad" \
  -d "NumMedia=0"
```

Expected XML response:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Response><Message>That sounds great! To find the best options for you, could you please share your approximate budget for the property?</Message></Response>
```

### ✅ Full Conversation Lead Qualification Flow

| Turn | User Sends | AI Behavior |
|------|------------|-------------|
| 1 | "I'm looking for a property" | Asks for location |
| 2 | "Akurdi" | Asks for property size (BHK) |
| 3 | "2 BHK" | Asks for budget |
| 4 | "Around 70 lakhs" | Confirms all 3 details, says agent will call within 1 minute |

### ✅ Check Docker Logs for Full Activity Trace

```bash
docker logs real_estate_ai_backend -f
```

You will see logs like:
```
Incoming WhatsApp from whatsapp:+91XXXXXXXXXX. Contains 0 media files.
AI Reply: Great! Could you tell me your preferred location...
```

---

## 📁 Project Structure

```
Real-Estate-AI-Agent-With-Devops/
│
├── main.py                  # FastAPI app — all webhook handlers and AI logic
├── requirements.txt         # Python dependencies
├── Dockerfile               # Container build instructions (Python 3.11-slim)
├── docker-compose.yaml      # Service definition: ports, env vars, volume mounts
├── Jenkinsfile              # 5-stage CI/CD pipeline definition
├── .env                     # ⚠️ YOUR secrets (not committed to Git)
└── static/                  # Auto-created: stores gTTS audio files at runtime
```

### Key Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/webhook/whatsapp` | Receives WhatsApp text and voice notes from Twilio |
| `POST` | `/webhook/voice` | Receives live phone call speech from Twilio |
| `GET`  | `/health` | Health check — confirms the server is running |

---

## 🔄 How It Works

### WhatsApp Text Flow

```
User sends text on WhatsApp
        ↓
Twilio POSTs to /webhook/whatsapp (Body = message text)
        ↓
FastAPI extracts Body field
        ↓
Sends to Groq LLaMA-3.3-70b with SYSTEM_PROMPT
        ↓
Returns TwiML <Response><Message>AI Reply</Message></Response>
        ↓
Twilio delivers reply to user's WhatsApp
```

### WhatsApp Voice Note Flow

```
User sends voice note on WhatsApp
        ↓
Twilio POSTs to /webhook/whatsapp (NumMedia=1, MediaUrl0=audio_url)
        ↓
FastAPI downloads OGG audio from MediaUrl0
        ↓
Sends audio to Groq Whisper → gets transcription text
        ↓
Sends transcription to LLaMA-3.3-70b → gets AI reply text
        ↓
Converts AI reply to MP3 audio using gTTS (Indian English)
        ↓
Saves MP3 to /static/, serves via StaticFiles
        ↓
Returns TwiML <Message><Media>audio_url</Media></Message>
        ↓
Twilio delivers MP3 as voice message on WhatsApp
```

### Live Phone Call Flow

```
User calls Twilio number
        ↓
Twilio POSTs to /webhook/voice (first call: SpeechResult is empty)
        ↓
Returns TwiML: <Gather input="speech"><Say>Greeting</Say></Gather>
        ↓
User speaks their response
        ↓
Twilio POSTs back to /webhook/voice (SpeechResult = spoken text)
        ↓
FastAPI sends text to LLaMA-3.3-70b
        ↓
Returns TwiML: <Gather><Say>AI Reply</Say></Gather>
        ↓
Loop continues until call ends
```

---

## 🔧 Troubleshooting

### Problem: Twilio webhook returns error / no reply

**Check 1:** Is the FastAPI server running?
```bash
curl http://localhost:8000/health
```

**Check 2:** Is Ngrok still running? The free tier resets URLs on restart.
```bash
# Restart ngrok and update Twilio webhook with new URL
ngrok http 8000
```

**Check 3:** Are there errors in the Docker logs?
```bash
docker logs real_estate_ai_backend -f
```

---

### Problem: `Error: 401 Unauthorized` from Groq API

Your Groq API key is incorrect or not set properly.

```bash
# Verify the key is being passed to the container
docker inspect real_estate_ai_backend | grep OPENAI_API_KEY
```

Make sure your `.env` file has no quotes around the key:
```env
# ✅ Correct
OPENAI_API_KEY=gsk_abc123...

# ❌ Wrong
OPENAI_API_KEY="gsk_abc123..."
```

---

### Problem: Jenkins build fails at Stage 5 (Deploy)

Ensure the Jenkins user has permission to run Docker commands:
```bash
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
```

---

### Problem: Voice note reply is missing / no audio returned

Check if the `static/` directory exists and is mounted:
```bash
ls -la static/
# Should contain .ogg and .mp3 files after a voice message is processed
```

If the directory is missing, Docker Compose will create it automatically on the next `up`.

---

### Problem: `python-multipart` not found

FastAPI uses `python-multipart` to parse Twilio's form-encoded webhook payloads. Make sure it's installed:
```bash
pip install python-multipart
# or rebuild Docker image after verifying requirements.txt
```

---

## 👤 Author

**Suyog Sachin Gampawar**
- 🎓 B.Tech AI & Data Science — Savitribai Phule Pune University (SPPU)
- 🐙 GitHub: [github.com/SUYOGGAMPAWAR](https://github.com/SUYOGGAMPAWAR)
- 💼 LinkedIn: [linkedin.com/in/suyog-gampawar-50ab66295](https://linkedin.com/in/suyog-gampawar-50ab66295)
- 📧 Email: suyoggampa@gmail.com

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

---

<p align="center">Built with ❤️ using FastAPI · Groq · Twilio · Docker · Jenkins</p>
